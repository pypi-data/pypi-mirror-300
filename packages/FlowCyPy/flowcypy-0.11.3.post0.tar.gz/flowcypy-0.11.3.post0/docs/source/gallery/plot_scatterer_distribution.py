"""
Flow Cytometry Simulation and 2D Hexbin Plot of Scattering Intensities
======================================================================

This script simulates a flow cytometer using the FlowCyPy library. It models light scattering from particles
detected by two detectors (Forward Scatter and Side Scatter) and visualizes the scattering intensities in a 2D hexbin plot.

Flow cytometry is used to analyze the physical and chemical properties of particles as they flow through a laser beam.

Steps in the Workflow:
----------------------
1. Define the flow parameters (e.g., speed, area, and total simulation time).
2. Create particle size and refractive index distributions.
3. Set up a laser source and detectors.
4. Simulate the flow cytometry experiment.
5. Visualize the scattering intensity in a 2D hexbin plot.
"""

# Import necessary libraries and modules
from FlowCyPy import Scatterer, FlowCell
from FlowCyPy import distribution
from FlowCyPy.population import Population
from FlowCyPy.units import second, nanometer, refractive_index_unit, particle, milliliter, meter, micrometer, millisecond
import numpy as np

# Set random seed for reproducibility
np.random.seed(20)

# Step 1: Define Flow Parameters
# ------------------------------
# The flow speed is set to 7.56 meters per second, with a flow area of 10 micrometers squared, and
# the total simulation time is 0.1 milliseconds.
flow = FlowCell(
    flow_speed=7.56 * meter / second,      # Flow speed: 7.56 meters per second
    flow_area=(10 * micrometer) ** 2,      # Flow area: 10 micrometers squared
    total_time=0.1 * millisecond           # Total simulation time: 0.1 milliseconds
)

# Step 2: Define Particle Size and Refractive Index Distributions
# ---------------------------------------------------------------
# Two particle populations are defined with different sizes and refractive indices.
lp_size = distribution.Normal(
    mean=200 * nanometer,                  # Liposome particle mean size: 200 nanometers
    std_dev=10 * nanometer                 # Liposome particle size standard deviation: 10 nanometers
)

ev_size = distribution.Normal(
    mean=50 * nanometer,                   # EV particle mean size: 50 nanometers
    std_dev=5.0 * nanometer                # EV particle size standard deviation: 5 nanometers
)

lp_ri = distribution.Normal(
    mean=1.45 * refractive_index_unit,     # Liposome refractive index mean: 1.45
    std_dev=0.01 * refractive_index_unit   # Liposome refractive index standard deviation: 0.01
)

ev_ri = distribution.Normal(
    mean=1.39 * refractive_index_unit,     # EV refractive index mean: 1.39
    std_dev=0.01 * refractive_index_unit   # EV refractive index standard deviation: 0.01
)

# Create populations of particles (liposomes and EVs) with defined sizes and refractive indices.
ev = Population(
    size=ev_size,                          # EV size distribution
    refractive_index=ev_ri,                # EV refractive index distribution
    concentration=1.8e+9 * particle / milliliter / 3,  # EV concentration
    name='EV'                              # Name of the EV population
)

lp = Population(
    size=lp_size,                          # Liposome size distribution
    refractive_index=lp_ri,                # Liposome refractive index distribution
    concentration=1.8e+9 * particle / milliliter / 1,  # Liposome concentration
    name='LP'                              # Name of the Liposome population
)

# %%
# Step 3: Create Scatterer Distribution
# -------------------------------------
# Combine the particle populations (liposomes and EVs) into a scatterer distribution within the flow.
scatterer = Scatterer(
    flow_cell=flow,                             # Flow parameters
    populations=[ev, lp]                   # List of populations: EVs and Liposomes
)

# Plot and visualize the scatterer distribution.
scatterer.plot()

# Display the properties of the scatterer distribution.
scatterer.print_properties()

"""
Summary:
--------
This script defines a flow cytometer simulation, sets up the particle size and refractive index distributions,
and visualizes the scatterer distribution in a 2D density plot. It provides insight into the scattering properties
of two different particle populations.
"""
