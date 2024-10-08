import laspy
import rasterio
import numpy as np
from time import time

from pypoints2grid import points2grid

las = laspy.read("pointcloud.las")
crs = las.header.parse_crs()

# filter out only ground (classififation 2) and water (classification 9)
ground = las.points[(las.classification == 2) | (las.classification == 9)]
pts = np.vstack((ground.x, ground.y, ground.z)).T

x_min, y_min, z_min = pts.min(axis=0)
x_max, y_max, z_max = pts.max(axis=0)

print(f"loaded {pts.shape[0]} points")
print(f"with bounnds: ({x_min}, {y_min}), ({x_max}, {y_max})")
cell_size = 0.5

print("creating grid")
start_time = time()
dem = points2grid(pts, cell_size)
print(
    f"created {dem.shape[0]}x{dem.shape[1]} grid from {pts.shape[0]} points in {round(time() - start_time, 2)} seconds"
)

transform = rasterio.transform.from_origin(x_min, y_max, cell_size, cell_size)

with rasterio.open(
    "dem.tif",
    "w",
    driver="GTiff",
    height=dem.shape[0],
    width=dem.shape[1],
    count=1,
    dtype=dem.dtype,
    crs=crs,
    transform=transform,
) as dst:
    dst.write(dem, 1)
