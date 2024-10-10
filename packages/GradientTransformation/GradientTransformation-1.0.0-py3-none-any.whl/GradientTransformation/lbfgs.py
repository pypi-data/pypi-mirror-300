# optimizer/lbfgs.py

import jax
import jax.numpy as jnp
from typing import Callable, Tuple, NamedTuple


class LbfgsState(NamedTuple):
    position: jnp.ndarray
    k: int
    s_list: jnp.ndarray
    y_list: jnp.ndarray
    rho_list: jnp.ndarray
    grad_f: jnp.ndarray
    converged: bool

class Lbfgs:
    def __init__(self, f: Callable[[jnp.ndarray], jnp.ndarray], m: int = 10, tol: float = 1e-6):
        """
        Initializes the L-BFGS gradient transformation.

        jit compatible

        Parameters:
        - f: Objective function to minimize.
        - m: int, Memory size (number of correction pairs).
        - tol: float, Tolerance for convergence.
        
        Note this will exit early if position is unchanged within E-20

        """
        self.f = f
        self.m = m
        self.tol = tol

    def init(self, x: jnp.ndarray) -> LbfgsState:
        """
        parameters:

        position: jnp.ndarray
        k: int
        s_list: jnp.ndarray
        y_list: jnp.ndarray
        rho_list: jnp.ndarray
        grad_f: jnp.ndarray
        converged: bool
        """
        return lbfgs_init(x, self.f, self.m)

    def update(self, state: LbfgsState) -> LbfgsState:
        state = lbfgs_update(self.f, self.tol, state)
        return state

def lbfgs_init(x0: jnp.ndarray, f: Callable[[jnp.ndarray], jnp.ndarray], m: int) -> LbfgsState:
    n = x0.shape[0]
    s_list = jnp.zeros((m, n))   # List to store past 's' vectors.
    y_list = jnp.zeros((m, n))   # List to store past 'y' vectors.
    rho_list = jnp.zeros(m)      # List to store scaling factors.
    grad_f = jax.grad(f)(x0)     # Compute the initial gradient.

    initial_state = LbfgsState(
        position=x0,
        k=0,
        s_list=s_list,
        y_list=y_list,
        rho_list=rho_list,
        grad_f=grad_f,
        converged=False
    )
    return initial_state

def lbfgs_update(
    f: Callable[[jnp.ndarray], jnp.ndarray],
    tol: float,
    state: LbfgsState,
    ) -> LbfgsState:
    """
    Performs a single L-BFGS update step.

    Parameters:
    - grads: Current gradients.
    - state: Current optimizer state.
    - f: Objective function.
    - m: Memory size.
    - tol: Tolerance for convergence.

    Returns:
    - updates: Parameter updates.
    - new_state: Updated optimizer state.
    """

    def lbfgs_false_branch(carry):
        return carry

    def lbfgs_true_branch(carry):
        position, s_list, y_list, rho_list, current_grad_f, k, converged = carry

        def gamma(carry):
            s_list, y_list = carry
            s = s_list[-1]
            y = y_list[-1]
            return jnp.dot(s, y) / jnp.dot(y,y)

        gamma = jax.lax.cond(k > 0, gamma, lambda s: 1.0, (s_list, y_list))
        # Hk = gamma * jnp.identity(position.shape[0]) #<--terrible for memory...
        Hk = gamma

        def compute_inverse_hessian_loop(carry, idx):
            def if_else(carry, idx):
                def true_branch(carry):
                    s_list, y_list, rho_list, alpha, grad = carry

                    # Get the current s, y, and rho values
                    s = s_list[idx]
                    y = y_list[idx]
                    rho = rho_list[idx]

                    # Compute alpha_i
                    alpha_i = rho * jnp.dot(s, grad)
                    
                    # Append alpha_i to the alpha list (or keep it in carry)
                    alpha = alpha.at[idx].set(alpha_i)

                    # Update q
                    grad = grad - alpha_i * y

                    # Return updated carry (q, alpha, ...)
                    return (s_list, y_list, rho_list, alpha, grad), None

                def false_branch(carry):
                    return carry, None
                s_list, y_list, rho_list, alpha, grad = carry
                return jax.lax.cond(jnp.sum(s_list[idx]) != 0.0, true_branch, false_branch, carry)
            return if_else(carry, idx)

        # We're dealing with the limited memory version so we have to ensure we don't loop over zeros at the beginning
        # Use jax.lax.scan to iterate over the indices in reverse order
        # Two-loop recursion to compute the approximate inverse Hessian product.
        num_loops = rho_list.shape[0]
        alpha = jnp.zeros(num_loops)  # To store alpha values
        grad = current_grad_f
        carry, _ = jax.lax.scan(compute_inverse_hessian_loop, (s_list, y_list, rho_list, alpha, grad), jnp.arange(num_loops-1, -1, -1))
        s_list, y_list, rho_list, alpha, grad = carry
       
        r = jnp.dot(Hk, grad)

        def search_direction(carry, idx):
            def if_else(carry, idx):
                def true_branch(carry):
                    s_list, y_list, rho_list, alpha, r = carry

                    # Get the current s, y, and rho values
                    s = s_list[idx]
                    y = y_list[idx]
                    rho = rho_list[idx]

                    beta = rho * jnp.dot(y, r)

                    alpha_i = alpha[idx]

                    r = r + s * (alpha_i - beta)

                    return (s_list, y_list, rho_list, alpha, r), None

                def false_branch(carry):
                    return carry, None
                s_list, y_list, rho_list, alpha, r = carry
                return jax.lax.cond(jnp.sum(s_list[idx]) != 0.0, true_branch, false_branch, carry)
            return if_else(carry, idx)

        carry, _ = jax.lax.scan(search_direction, (s_list, y_list, rho_list, alpha, r), jnp.arange(num_loops))
        s_list, y_list, rho_list, alpha, r = carry
        pK = -1 * r
        step_size = 1.0       # Initial step size.
        c1 = 1e-4             # Parameter for sufficient decrease (Armijo condition).

        def inner_while_loop_condition(carry):
            position, current_grad_f, step_size, c1, pK = carry
            return jnp.logical_and(f(position + step_size * pK) > f(position) + c1 * step_size * jnp.dot(current_grad_f, pK),
                                  step_size >= jnp.float32(1e-8))

        def inner_while_loop_body(carry):
            position, current_grad_f, step_size, c1, pK = carry
            step_size = step_size * 0.5                    # Reduce step size.
            return position, current_grad_f, step_size, c1, pK

        carry = jax.lax.while_loop(inner_while_loop_condition, inner_while_loop_body, (position, current_grad_f, step_size, c1, pK))
        position, current_grad_f, step_size, c1, pK = carry

        # Update position and gradient.
        position_new = position + step_size * pK              # Update position.
        grad_new = jax.grad(f)(position_new)                  # Compute new gradient.
        sk = position_new - position                          # Compute s_k.
        converged = jnp.all(jnp.isclose(sk, 0.0, atol=1e-20)) # exit early if the solution is converged
        yk = grad_new - current_grad_f                        # Compute y_k.

        # Update s_list, y_list, rho_list
        def true_branch(carry):
            s_list, y_list, rho_list, sk, yk = carry
            # If history is full, remove the oldest
            s_list = jnp.roll(s_list, shift=-1, axis=0)
            y_list = jnp.roll(y_list, shift=-1, axis=0)
            rho_list = jnp.roll(rho_list, shift=-1)
            # Set the latest entry
            s_list = s_list.at[-1].set(sk)
            y_list = y_list.at[-1].set(yk)
            rho_list = rho_list.at[-1].set(1.0/jnp.dot(yk,sk))

            return s_list, y_list, rho_list, sk, yk  

        def false_branch(carry):
            return carry

        # Update the state
        carry = jax.lax.cond(jnp.dot(sk,yk) > jnp.float32(1e-10), true_branch, false_branch, (s_list, y_list, rho_list, sk, yk))
        s_list, y_list, rho_list, sk, yk = carry

        position = position_new
        current_grad_f = grad_new
        k = k + 1

        return (position, s_list, y_list, rho_list, current_grad_f, k, converged)

    # Unpack the state
    position = state.position
    s_list = state.s_list
    y_list = state.y_list
    rho_list = state.rho_list
    current_grad_f = state.grad_f
    k = state.k
    converged = state.converged

    def lbfgs_condition_iter(state):
        # Unpack the state
        position = state.position
        s_list = state.s_list
        y_list = state.y_list
        rho_list = state.rho_list
        current_grad_f = state.grad_f
        k = state.k
        converged = state.converged
        carry = (position, s_list, y_list, rho_list, current_grad_f, k, converged)

        final_state = jax.lax.cond(jnp.logical_and(jnp.linalg.norm(current_grad_f) > tol, converged == False),
                                   lbfgs_true_branch, lbfgs_false_branch, carry)
        return final_state

    final_state = lbfgs_condition_iter(state)
    position, s_list, y_list, rho_list, current_grad_f, k, converged = final_state
    final_state = LbfgsState(
        position=position,
        k=k,
        s_list=s_list,
        y_list=y_list,
        rho_list=rho_list,
        grad_f=current_grad_f,
        converged=converged
    )

    return final_state
