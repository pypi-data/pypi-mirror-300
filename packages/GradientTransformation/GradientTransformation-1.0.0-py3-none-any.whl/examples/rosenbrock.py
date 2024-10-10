import jax
import jax.numpy as jnp
from GradientTransformation import Lbfgs

def n_dim_rosenbrock(x: jnp.ndarray, dtype= jnp.float32) -> jnp.ndarray:
    """
    Generalized n-dimensional Rosenbrock function.

    minimum is every position of input vector equal to 1.
    """
    result =  jnp.sum(100.0 * (x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0)
    return jnp.asarray(result, dtype=dtype)

def main():
    # Define the loss function
    def loss(x):
        return n_dim_rosenbrock(x)

    # Initialize parameters near the local maximum
    n = 1000
    # Initialize PRNG key
    key = jax.random.PRNGKey(42)

    # Split the key
    key1, _ = jax.random.split(key, 2)    # Initialize PRNG key
    x0 = jax.random.uniform(key1, shape=(n,), minval=-4, maxval=4)

    # Instantiate the L-BFGS optimizer
    optimizer = Lbfgs(f=loss, m=10, tol=1e-6)

    # Initialize optimizer state
    opt_state = optimizer.init(x0)

    @jax.jit
    def opt_step(carry, _):
        opt_state, losses = carry
        opt_state = optimizer.update(opt_state)
        losses = losses.at[opt_state.k].set(loss(opt_state.position))
        return (opt_state, losses), _

    iterations=10000
    losses = jnp.zeros((iterations,))
    (final_state, losses), _ = jax.lax.scan(opt_step, (opt_state,losses), None, length=iterations)
    losses = jnp.array(jnp.where(losses == 0, jnp.nan, losses))

    print(final_state)

    print("Estimated minimum position:", final_state.position)
    print("Function value at minimum:", loss(final_state.position))
    print("k: ", final_state.k)
    # print("_______________________________________")

if __name__ == "__main__":
    main()
