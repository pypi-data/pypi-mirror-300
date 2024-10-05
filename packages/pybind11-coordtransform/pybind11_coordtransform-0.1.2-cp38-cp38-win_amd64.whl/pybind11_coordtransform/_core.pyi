"""

        c++/python version of https://github.com/wandergis/coordtransform

"""
from __future__ import annotations
import numpy

__all__ = [
    "bd09togcj02",
    "gcj02_to_wgs84_Nx2",
    "gcj02_to_wgs84_Nx3",
    "gcj02tobd09",
    "gcj02towgs84",
    "out_of_china",
    "wgs84_to_gcj02_Nx2",
    "wgs84_to_gcj02_Nx3",
    "wgs84togcj02",
]

def bd09togcj02(lng: float, lat: float) -> numpy.ndarray[numpy.float64[2, 1]]:
    """
    Convert BD09 coordinates to GCJ02 coordinates.

    Args:
        lng (float): Longitude in BD09 coordinate system.
        lat (float): Latitude in BD09 coordinate system.

    Returns:
        tuple: A tuple containing (longitude, latitude) in GCJ02 coordinate system.
    """

def gcj02_to_wgs84_Nx2(
    coords: numpy.ndarray[numpy.float64[m, 2]], check_out_of_china: bool = True
) -> numpy.ndarray[numpy.float64[m, 2]]:
    """
    Convert multiple GCJ02 coordinates to WGS84 coordinates (for Nx2 matrices).

    Args:
        coords (numpy.ndarray): Nx2 array of coordinates in GCJ02 system.
        check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

    Returns:
        numpy.ndarray: Nx2 array of coordinates in WGS84 system.
    """

def gcj02_to_wgs84_Nx3(
    coords: numpy.ndarray[numpy.float64[m, 3]], check_out_of_china: bool = True
) -> numpy.ndarray[numpy.float64[m, 3]]:
    """
    Convert multiple GCJ02 coordinates to WGS84 coordinates (for Nx3 matrices).

    Args:
        coords (numpy.ndarray): Nx3 array of coordinates in GCJ02 system.
        check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

    Returns:
        numpy.ndarray: Nx3 array of coordinates in WGS84 system.
    """

def gcj02tobd09(lng: float, lat: float) -> numpy.ndarray[numpy.float64[2, 1]]:
    """
    Convert GCJ02 coordinates to BD09 coordinates.

    Args:
        lng (float): Longitude in GCJ02 coordinate system.
        lat (float): Latitude in GCJ02 coordinate system.

    Returns:
        tuple: A tuple containing (longitude, latitude) in BD09 coordinate system.
    """

def gcj02towgs84(
    lng: float, lat: float, check_out_of_china: bool = True
) -> numpy.ndarray[numpy.float64[2, 1]]:
    """
    Convert GCJ02 coordinates to WGS84 coordinates.

    Args:
        lng (float): Longitude in GCJ02 coordinate system.
        lat (float): Latitude in GCJ02 coordinate system.
        check_out_of_china (bool, optional): If True, check if the coordinates are outside China. Defaults to True.

    Returns:
        tuple: A tuple containing (longitude, latitude) in WGS84 coordinate system.
    """

def out_of_china(lng: float, lat: float) -> bool:
    """
    Check if the given coordinates are outside China.

    Args:
        lng (float): Longitude.
        lat (float): Latitude.

    Returns:
        bool: True if the coordinates are outside China, False otherwise.
    """

def wgs84_to_gcj02_Nx2(
    coords: numpy.ndarray[numpy.float64[m, 2]], check_out_of_china: bool = True
) -> numpy.ndarray[numpy.float64[m, 2]]:
    """
    Convert multiple WGS84 coordinates to GCJ02 coordinates (for Nx2 matrices).

    Args:
        coords (numpy.ndarray): Nx2 array of coordinates in WGS84 system.
        check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

    Returns:
        numpy.ndarray: Nx2 array of coordinates in GCJ02 system.
    """

def wgs84_to_gcj02_Nx3(
    coords: numpy.ndarray[numpy.float64[m, 3]], check_out_of_china: bool = True
) -> numpy.ndarray[numpy.float64[m, 3]]:
    """
    Convert multiple WGS84 coordinates to GCJ02 coordinates (for Nx3 matrices).

    Args:
        coords (numpy.ndarray): Nx3 array of coordinates in WGS84 system.
        check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

    Returns:
        numpy.ndarray: Nx3 array of coordinates in GCJ02 system.
    """

def wgs84togcj02(
    lng: float, lat: float, check_out_of_china: bool = True
) -> numpy.ndarray[numpy.float64[2, 1]]:
    """
    Convert WGS84 coordinates to GCJ02 coordinates.

    Args:
        lng (float): Longitude in WGS84 coordinate system.
        lat (float): Latitude in WGS84 coordinate system.
        check_out_of_china (bool, optional): If True, check if the coordinates are outside China. Defaults to True.

    Returns:
        tuple: A tuple containing (longitude, latitude) in GCJ02 coordinate system.
    """

__version__: str = "0.1.2"
