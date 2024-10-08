import numpy as np
from FlowCyPy import Scatterer, Detector, Source
from FlowCyPy import ureg
from PyMieSim.single.scatterer import Sphere as PMS_SPHERE
from PyMieSim.single.source import Gaussian as PMS_GAUSSIAN
from PyMieSim.single.detector import Photodiode as PMS_PHOTODIODE
from FlowCyPy.units import meter, watt, degree

def compute_detected_signal(source: Source, detector: Detector, scatterer: Scatterer) -> float:
    """
    Empirical model for scattering intensity based on particle size, granularity, and detector angle.

    This function models forward scatter (FSC) as proportional to the particle's size squared and
    side scatter (SSC) as proportional to the granularity and modulated by angular dependence
    (sin^n(theta)). Granularity is a dimensionless measure of the particle's internal complexity or
    surface irregularities:

    - A default value of 1.0 is used for moderate granularity (e.g., typical white blood cells).
    - Granularity values < 1.0 represent smoother particles with less internal complexity (e.g., bacteria).
    - Granularity values > 1.0 represent particles with higher internal complexity or surface irregularities (e.g., granulocytes).

    Parameters
    ----------
    detector : Detector
        The detector object containing phi_angle (in radians).
    particle_size : float
        The size of the particle (in meters).
    granularity : float, optional
        A measure of the particle's internal complexity or surface irregularities (dimensionless).
        Default is 1.0.
    A : float, optional
        Empirical scaling factor for angular dependence. Default is 1.5.
    n : float, optional
        Power of sine function for angular dependence. Default is 2.0.

    Returns
    -------
    Quantity
        The detected scattering intensity for the given particle and detector.
    """
    from PyMieSim.units import degree
    pms_source = PMS_GAUSSIAN(
        wavelength=source.wavelength,
        polarization=source.polarization,
        optical_power=source.optical_power,
        NA=source.numerical_aperture
    )

    size_list = scatterer.dataframe['Size']
    ri_list = scatterer.dataframe['RefractiveIndex']
    couplings = np.empty_like(size_list).astype(float)

    _cache = {}

    for index, (size, ri) in enumerate(zip(size_list, ri_list)):
        # Create a unique cache key based on (size, ri)
        cache_key = (size, ri)

        # Check if result is already in cache
        if cache_key in _cache:
            couplings[index] = _cache[cache_key]
        else:
            # If not cached, compute the scattering and store it in the cache
            pms_scatterer = PMS_SPHERE(
                diameter=size,
                property=ri,
                medium_property=scatterer.medium_refractive_index,
                source=pms_source
            )

            pms_detector = PMS_PHOTODIODE(
                NA=detector.numerical_aperture,
                gamma_offset=detector.gamma_angle,
                phi_offset=detector.phi_angle,
                polarization_filter=None,
                sampling=detector.sampling
            )

            # Compute the coupling and store it in the cache
            coupling_value = pms_detector.coupling(pms_scatterer)
            couplings[index] = coupling_value
            _cache[cache_key] = coupling_value  # Cache the result

    return couplings * ureg.watt
