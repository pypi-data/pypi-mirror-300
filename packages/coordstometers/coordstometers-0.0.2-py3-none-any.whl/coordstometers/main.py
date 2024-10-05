import numpy as np

# NOTE: GPS coords go lat-lon, meter coords go lon-lat because longitude is horizontal.


def get_scale(center_coord: np.ndarray) -> np.ndarray:
    """
    Returns the scaling factor for converting differences in latitude and longitude
    near a certain coordinate to distances in meters.


    Parameters:
        center_coord: A numpy array of shape (2,) representing the (latitude, longitude) of the center point.

    Returns:
        A numpy array with the scale factors for latitude and longitude differences.
    """
    if center_coord.shape != (2,):
        raise ValueError(
            "center_coord must be a 1D array of shape (2,) representing (latitude, longitude)."
        )

    earth_circumference = 40030174  # Circumference of the Earth in meters
    lat_scale = earth_circumference / 360  # Conversion for latitude
    lon_scale = lat_scale * np.cos(
        np.deg2rad(center_coord[0])
    )  # Conversion for longitude based on latitude
    return np.array([lat_scale, lon_scale])


def coords_to_meters(pts_lat_lon: np.ndarray, center_coord: np.ndarray) -> np.ndarray:
    """
    Converts latitude and longitude coordinates to meters relative to a center point.

    Parameters:
        pts_lat_lon: A numpy array of shape (n, 2) with latitude and longitude points.
        center_coord: A numpy array of shape (2,) representing the (latitude, longitude) of the center point.

    Returns:
        A numpy array of shape (n, 2) with the converted points in meters.
    """
    if pts_lat_lon.shape[1] != 2:
        raise ValueError("pts_lat_lon must be a 2D array with shape (n, 2).")

    if center_coord.shape != (2,):
        raise ValueError(
            "center_coord must be a 1D array of shape (2,) representing (latitude, longitude)."
        )

    pts_inter = pts_lat_lon - center_coord  # Translate points relative to the center
    pts_inter *= get_scale(center_coord)  # Scale points to meters
    pts_meters = pts_inter[:, ::-1]  # Swap x and y (lon-lat to meters format)
    return pts_meters


def meters_to_coords(pts_meters: np.ndarray, center_coord: np.ndarray) -> np.ndarray:
    """
    Converts coordinates in meters to latitude and longitude given a latitude and longitude center point.

    Parameters:
        pts_meters: A numpy array of shape (n, 2) with points in meters.
        center_coord: A numpy array of shape (2,) representing the (latitude, longitude) of the center point.

    Returns:
        A numpy array of shape (n, 2) with the converted points in latitude and longitude.
    """
    if pts_meters.shape[1] != 2:
        raise ValueError("pts_meters must be a 2D array with shape (n, 2).")

    if center_coord.shape != (2,):
        raise ValueError(
            "center_coord must be a 1D array of shape (2,) representing (latitude, longitude)."
        )

    pts_inter = pts_meters[:, ::-1]  # Swap x and y (meters to lon-lat format)
    pts_inter /= get_scale(center_coord)  # Scale points back to lat-lon
    pts_lat_lon = pts_inter + center_coord  # Translate points back to original position
    return pts_lat_lon
