import sys
import os

# Append the path to src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Now you can import coordstometers
import coordstometers
import numpy as np


def main():
    # these points are about 2 miles or 3280 meters apart
    p1 = np.array([39.951382247305865, -75.18069081865926])
    p2 = np.array([39.946669181885326, -75.14280990491913])
    pts = np.array([p1, p2])
    target_dist = 3280

    center = np.mean(pts, axis=0)
    pts_meters = coordstometers.coords_to_meters(pts, center)

    # get the distance between them
    dist = np.linalg.norm(pts_meters[0] - pts_meters[1])
    if np.isclose(dist, target_dist, atol=100):
        print(
            f"Test passed, distance is {round(dist)} meters which is not too far from {target_dist} meters"
        )
    else:
        print(
            f"Test failed, distance is {dist} meters which is not close to {target_dist} meters"
        )

    # convert back to lat lon
    pts_lat_lon = coordstometers.meters_to_coords(pts_meters, center)
    # check if the points are the same
    if np.allclose(pts, pts_lat_lon):
        print("Test passed, points are the same after conversion")
    else:
        print("Test failed, points are not the same after conversion")


if __name__ == "__main__":
    main()
