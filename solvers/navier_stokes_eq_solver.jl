# 1. Install packages if needed:
# using Pkg; Pkg.add(["WaterLily", "GLMakie"])

using WaterLily
using GLMakie

# Define a 3D Taylor-Green Vortex setup
function taylor_green(N=64; Re=100)
    # Define initial velocity field mapping (x, t) -> u_vector
    # TGV analytical formulation for 3D
    function u(i, x, t)
        if i == 1
            return  sin(x[1]) * cos(x[2]) * cos(x[3])
        elseif i == 2
            return -cos(x[1]) * sin(x[2]) * cos(x[3])
        else
            return 0.0
        end
    end
    # Create the 3D simulation box
    return Simulation((N, N, N), (0.0, 0.0, 0.0), 1.0; u=u, ν=1/Re)
end

# 2. Set up the solver and grid
N = 48
sim = taylor_green(N, Re=500)

# Extract a 3D matrix containing the velocity magnitude or vorticity
# For simplicity, let's grab the U-component velocity grid
u_component = Observable(sim.flow.u[:, :, :, 1]) 

# 3. Create the interactive 3D Plot
fig = Figure(resolution = (800, 600))
ax = Axis3(fig[1, 1], title = "3D Navier-Stokes (Velocity Component)")

# Volume rendering plots a semi-transparent 3D density cloud
volume!(ax, 1:N, 1:N, 1:N, u_component, colormap = :vibrant)

display(fig)

# 4. Time-stepping loop to animate the Navier-Stokes evolution
for step in 1:100
    sim_step!(sim, 0.1) # Step forward in time by dt=0.1
    u_component[] = sim.flow.u[:, :, :, 1] # Update the plotting observable
    sleep(0.01)
end
