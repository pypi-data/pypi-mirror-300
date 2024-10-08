#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Tools for solar energy analysis.

Connects Salient timeseries data to pvlib.
https://salientpredictions.atlassian.net/browse/RD-1259
"""

# import matplotlib.pyplot as plt
import pandas as pd
import pvlib as pv
import requests
import xarray as xr

from .data_timeseries_api import data_timeseries, load_multihistory
from .downscale_api import downscale
from .geo_api import add_geo
from .location import Location

SOLAR_VARIABLES = ["temp", "wspd", "tsi", "dhi", "dni"]


def data_timeseries_solar(
    # API inputs -------
    loc: Location,
    start: str = "1950-01-01",
    end: str = "-today",
    variable: list[str] = SOLAR_VARIABLES,
    debias: bool = False,
    # non-API arguments ---
    destination: str = "-default",
    force: bool = False,
    session: requests.Session | None = None,
    apikey: str | None = None,
    verify: bool | None = None,
    verbose: bool = False,
) -> xr.Dataset:
    """Get a historical time series of pvlib-compatible solar weather inputs.

    A convenience wrapper around `data_timeseries()` to get solar weather data.
    Generates a past weather dataset suitable to pass to `run_pvlib_dataset()`.

    Args:
        loc (Location): The location to query.
        start (str): The start date of the time series
        end (str): The end date of the time series
        variable (list[str]): The variables to download.
            Defaults to `["temp", "wspd", "tsi", "dhi", "dni"]` which are the inputs
            needed for `run_pvlib_dataset()`.
        debias (bool): If `True`, debias the data to local observations.
            Defaults to `False` since debiasing does not currently support
            solar components like `tsi`, `dhi`, and `dni`.

        destination (str): The directory to download the data to
        force (bool): If False (default), don't download the data if it already exists
        session (requests.Session): The session object to use for the request.
            If `None` (default) uses `get_current_session()`.
        apikey (str | None): The API key to use for the request.
            In most cases, this is not needed if a `session` is provided.
        verify (bool): If True (default), verify the SSL certificate
        verbose (bool): If True (default False) print status messages

    Returns:
        xr.Dataset: An hourly dataset with the following variables:
            - temp: temperature (C)
            - wspd: wind speed (m/s)
            - tsi: total solar irradiance, aka Global Horizontal Irradiance (W/m^2)
            - dhi: diffuse horizontal irradiance (W/m^2)
            - dni: direct normal irradiance (W/m^2)
            - elevation: elevation (m)
    """
    field = "vals"
    format = "nc"
    frequency = "hourly"
    # units = "SI" - unnecessary, since it's the default
    file = data_timeseries(**locals())
    vals = load_multihistory(file)
    vals = add_geo(
        loc=loc,
        ds=vals,
        variables="elevation",
        destination=destination,
        force=force,
        session=session,
        apikey=apikey,
        verify=verify,
        verbose=verbose,
    )

    return vals


def downscale_solar(
    # API inputs -------
    loc: Location,
    date: str = "-today",
    members: int = 50,
    variables: list[str] = SOLAR_VARIABLES,
    # non-API arguments ---
    destination: str = "-default",
    force: bool = False,
    session: requests.Session | None = None,
    apikey: str | None = None,
    verify: bool | None = None,
    verbose: bool = False,
    **kwargs,
) -> xr.Dataset:
    """Get a forecast time series of pvlib-compatible solar weather inputs.

    A convenience wrapper around `downscale()` to get solar weather data.
    Generates a future weather dataset suitable to pass to `run_pvlib_dataset()`.

    Status: development experimental.

    Args:
        loc (Location): The location to query.
        date (str): The start date of the time series.
            If `date` is `-today`, use the current date.
        members (int): The number of ensemble members to download
        variables (list[str]): The variables to download.
            Defaults to `["temp", "wspd", "tsi", "dhi", "dni"]` which are the inputs
            needed for `run_pvlib_dataset()`.

        destination (str): The directory to download the data to
        force (bool): If False (default), don't download the data if it already exists
        session (requests.Session): The session object to use for the request.
            If `None` (default) uses `get_current_session()`.
        apikey (str | None): The API key to use for the request.
            In most cases, this is not needed if a `session` is provided.
        verify (bool): If True (default), verify the SSL certificate
        verbose (bool): If True (default False) print status messages
        **kwargs: Additional arguments to pass to `downscale()`

    Keyword Arguments:
        reference_clim (str): Reference period to calculate anomalies.
        version (str): The model version of the Salient `blend` forecast.
        debias (bool): Defaults to `False`, note that `tsi`, `dhi`, and `dni` are not debiased.


    Returns:
        xr.Dataset: An hourly dataset with the following variables:
            - temp: temperature (C)
            - wspd: wind speed (m/s)
            - tsi: total solar irradiance, aka Global Horizontal Irradiance (W/m^2)
            - dhi: diffuse horizontal irradiance (W/m^2)
            - dni: direct normal irradiance (W/m^2)
            - elevation: elevation (m)
    """
    frequency = "hourly"
    # units = "SI" unnecessary since it's the default
    file = downscale(**{**{k: v for k, v in locals().items() if k != "kwargs"}, **kwargs})
    # enhancement: if "location" is vectorized, need to load multiple datasets:
    vals = xr.load_dataset(file)

    vals = add_geo(
        loc=loc,
        ds=vals,
        variables="elevation",
        destination=destination,
        force=force,
        session=session,
        apikey=apikey,
        verify=verify,
        verbose=verbose,
    )

    return vals


def run_pvlib_dataset(
    weather: xr.Dataset | str, timedim: str = "time", mc: pv.modelchain.ModelChain | None = None
):
    """Execute pvlib multiple times on a weather-inputs dataset.

    Args:
        weather (xr.Dataset | str): Solar meteorological inputs,
            of the form returned by `data_timeseries_solar()`
            May also be the filename to a valid dataset.
        timedim (str): The name of the time dimension
        mc (pv.modelchain.ModelChain): The model chain to use.  If `None`, a default is used.

    Returns:
        xr.Dataset: A dataset with matching coordinates to `ds` containing
            `ac`, `dc`, and `effective_irradiance` as data variables
    """
    if isinstance(weather, str):
        weather = xr.open_dataset(weather)

    (ac, dc, ei) = xr.apply_ufunc(
        _run_pvlib_slice,
        weather[timedim],
        weather["tsi"],
        weather["dhi"],
        weather["dni"],
        weather["temp"],
        weather["wspd"],
        weather["lat"],
        weather["lon"],
        weather["elevation"],
        mc,
        input_core_dims=[
            [timedim],  # time
            [timedim],  # tsi
            [timedim],  # dhi
            [timedim],  # dni
            [timedim],  # temp
            [timedim],  # wspd
            [],  # lat
            [],  # lon
            [],  # elev
            [],  # mc
        ],
        output_core_dims=[[timedim], [timedim], [timedim]],
        vectorize=True,
    )

    pwr = xr.Dataset(
        {"ac": ac, "dc": dc, "effective_irradiance": ei},
        coords=weather.coords,
    )
    pwr["ac"].attrs = {"units": "W", "long_name": "AC Power", "standard_name": "ac"}

    pwr["dc"].attrs = {"units": "W", "long_name": "DC Power", "standard_name": "dc"}

    pwr["effective_irradiance"].attrs = {
        "units": "W m**-2",
        "long_name": "Effective Irradiance",
        "standard_name": "effective_irradiance",
    }
    return pwr


def _run_pvlib_slice(
    time: list[float],  # "time",
    tsi: list[float],  # "ghi",
    dhi: list[float],  # "dhi",
    dni: list[float],  # "dni",
    temp: list[float],  # "temp_air",
    wspd: list[float],  # "wind_speed",
    lat: float,  # "latitude",
    lon: float,  # "longitude",
    elev: float = 0,  # "altitude",
    mc: pv.modelchain.ModelChain | None = None,
) -> tuple[list[float], list[float], list[float]]:
    """Run a single instance of a pvlib model chain.

    Intended to be called inside a ufunc to iterate over multiple
    lat/lon locations and also downscale ensembles.
    """
    # Assemble all of the columns into a single pandas dataframe
    weather = pd.DataFrame(
        {
            "ghi": tsi,
            "dhi": dhi,
            "dni": dni,
            "temp_air": temp,
            "wind_speed": wspd,
        },
        index=pd.to_datetime(time, utc=True),
    )

    if mc is None:
        mc = _get_default_modelchain(lat, lon, elev)
    else:
        mc.location = pv.location.Location(lat, lon, tz="UTC", altitude=elev)

    mc.run_model(weather)

    return mc.results.ac, mc.results.dc, mc.results.effective_irradiance


def _get_default_modelchain(lat=33, lon=-97, elev=0):
    """Get a standardized pvlib model chain."""
    arrays = pv.pvsystem.Array(
        pv.pvsystem.FixedMount(lat, 180 if lat > 0 else 0),
        name="Array",
        module_parameters=dict(pdc0=1, gamma_pdc=-0.004),
        temperature_model_parameters=dict(a=-3.56, b=-0.075, deltaT=3),
    )
    loc = pv.location.Location(lat, lon, tz="UTC", altitude=elev)
    system = pv.pvsystem.PVSystem(arrays=arrays, inverter_parameters=dict(pdc0=3))
    mc = pv.modelchain.ModelChain(system, loc, aoi_model="physical", spectral_model="no_loss")

    return mc
