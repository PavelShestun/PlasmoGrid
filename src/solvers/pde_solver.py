import numpy as np
from scipy.ndimage import laplace

class PDESolver:
    """
    Solves the continuous Physarum model using the Finite Difference Method.
    """
    def __init__(self, grid_size=(100, 100), sources_sinks=None, resistance_field=None):
        self.grid_size = grid_size
        self.mu = np.ones(grid_size)  # Conductivity field
        self.u = np.zeros(grid_size)   # Potential field

        self.f = np.zeros(grid_size)  # Sources and sinks
        if sources_sinks:
            for (x, y), val in sources_sinks.items():
                self.f[x, y] = val

        self.k = np.ones(grid_size)   # Resistance field
        if resistance_field is not None:
            self.k = resistance_field

    def run_simulation(self, num_iterations, dt=0.1):
        """
        Run the simulation for a number of iterations.
        """
        for _ in range(num_iterations):
            self._solve_potential()
            self._update_conductivity(dt)

    def _solve_potential(self):
        """
        Solves the elliptic equation for the potential field u using Jacobi iteration.
        -∇ ⋅ (μ ∇u) = f  =>  ∇μ ⋅ ∇u + μ ∇²u = -f
        """
        # We use a simple Jacobi iteration to solve the Poisson-like equation
        # This is a simplification and a more robust solver would be needed for complex cases
        for _ in range(50): # 50 Jacobi iterations
            grad_mu_y, grad_mu_x = np.gradient(self.mu)
            grad_u_y, grad_u_x = np.gradient(self.u)

            laplacian_u = laplace(self.u)

            # Update u based on the discretized PDE
            # Simplified to μ ∇²u ≈ -f for stability
            new_u = self.u - 0.01 * (self.mu * laplacian_u + self.f)

            # Boundary conditions (Dirichlet, u=0 at boundaries) could be added here
            self.u = np.nan_to_num(new_u)


    def _update_conductivity(self, dt):
        """
        Updates the conductivity field μ based on the potential field u.
        μ' = μ * (|∇u| - k)
        """
        grad_u_y, grad_u_x = np.gradient(self.u)
        grad_u_magnitude = np.sqrt(grad_u_x**2 + grad_u_y**2)

        dmu_dt = self.mu * (grad_u_magnitude - self.k)
        self.mu += dt * dmu_dt
        self.mu = np.clip(self.mu, 1e-6, None) # Prevent mu from becoming zero or negative
