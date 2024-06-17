import os
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.merge import merge
import rioxarray
from shapely.geometry import Polygon
import netCDF4 as nc
import pandas as pd

# TODO : define some custom logic
def custom_logic():
    pass


def create_mosaic_from_folder(
        input_folder: str, 
        output_folder: str, 
        output_filename: str
    ) -> None:
    """
    Create a mosaic from TIFF files in the input folder and save it to the output folder with the specified filename.

    Parameters:
        input_folder (str): Path to the folder containing TIFF files.
        output_folder (str): Path to the folder where the final mosaic TIFF will be saved.
        output_filename (str): Name of the final mosaic TIFF file.
    """
    input_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.tif')]
    src_files_to_mosaic = []

    try:
        for input_tiff in input_files:
            src = rasterio.open(input_tiff)
            src_files_to_mosaic.append(src)

        merged_data, merged_transform = merge(src_files_to_mosaic)
        output_profile = src_files_to_mosaic[0].profile

        output_profile.update({
            "transform": merged_transform,
            "height": merged_data.shape[1],
            "width": merged_data.shape[2]
        })

        os.makedirs(output_folder, exist_ok=True)
        output_tiff = os.path.join(output_folder, output_filename)

        with rasterio.open(output_tiff, "w", **output_profile) as dst:
            dst.write(merged_data)

        print(f"Mosaic created and saved at: {output_tiff}")

    except Exception as e:
        print(f"An error occurred during mosaic creation: {e}")

    finally:
        for src in src_files_to_mosaic:
            src.close()


def process_single_file(
        file_path: str, 
        output_dir: str, 
        target_x_pixel_size: float
    ) -> None:
    """
    Process a single NetCDF file to extract relevant data and save it as a GeoTIFF file.

    Parameters:
        file_path (str): Path to the NetCDF file.
        output_dir (str): Directory to save the processed GeoTIFF file.
        target_x_pixel_size (float): Target pixel size for the output GeoTIFF file.
    """
    file_name = os.path.basename(file_path)
    product_name = file_name

    climate_filepath = os.path.join(file_path, "LST_in.nc")
    cart_filepath = os.path.join(file_path, "geodetic_in.nc")
    flags_filepath = os.path.join(file_path, "flags_in.nc")

    with nc.Dataset(cart_filepath, 'r') as ncfile:
        latitude = ncfile.variables["latitude_in"][:]
        longitude = ncfile.variables["longitude_in"][:]

    with nc.Dataset(climate_filepath, 'r') as ncfile:
        lst = ncfile.variables["LST"][:]

    with nc.Dataset(flags_filepath, 'r') as ncfile:
        bayes_in = ncfile.variables["bayes_in"][:].flatten()
        confidence_in = ncfile.variables["confidence_in"][:].flatten()

    lst = lst - 273.15

    lst_df = pd.DataFrame({
        'lon': longitude.flatten(),
        'lat': latitude.flatten(),
        'LST': lst.flatten()
    })

    mask = (bayes_in == 2) | (confidence_in == 16384)
    lst_df.loc[mask, 'LST'] = np.nan

    y_pixel_size = target_x_pixel_size
    x_pixel_size = target_x_pixel_size

    ncol = int((longitude.max() - longitude.min()) / x_pixel_size)
    nrow = int((latitude.max() - latitude.min()) / y_pixel_size)

    lst_df['geometry'] = [Polygon(
        [(lon, lat), (lon + x_pixel_size, lat), (lon + x_pixel_size, lat - y_pixel_size), (lon, lat - y_pixel_size)]
    ) for lon, lat in zip(lst_df['lon'], lst_df['lat'])]

    os.makedirs(output_dir, exist_ok=True)
    output_raster = f"{product_name}.tif"
    output_path = os.path.join(output_dir, output_raster)

    with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=nrow,
            width=ncol,
            count=1,
            dtype=rasterio.float64,
            crs='EPSG:4326',
            transform=rasterio.transform.from_origin(longitude.min(), latitude.max(), x_pixel_size, y_pixel_size),
    ) as dst:
        shapes = ((geom, val) for geom, val in zip(lst_df['geometry'], lst_df['LST']))
        burned = rasterio.features.rasterize(
            shapes=shapes,
            out_shape=(nrow, ncol),
            transform=rasterio.transform.from_origin(longitude.min(), latitude.max(), x_pixel_size, y_pixel_size),
            all_touched=True
        )
        dst.write(burned, 1)

    print(f"Processed file: {file_name}")


def clip_tiff_files(
    output_filename: str,
    shapefile_path: str,
    tiff_file: str
) -> None:
    """
    Clip a TIFF file using the geometries from a shapefile and save the clipped result.

    Parameters:
        output_filename (str): Path to save the clipped TIFF file.
        shapefile_path (str): Path to the shapefile containing clipping geometries.
        tiff_file (str): Path to the TIFF file to be clipped.
    """
    try:
        # Read the shapefile and reproject it to the CRS of the TIFF file
        gdf = gpd.read_file(shapefile_path)
        tiff_crs = rioxarray.open_rasterio(tiff_file).rio.crs
        gdf = gdf.to_crs(tiff_crs)

        clip_geometry = gdf.geometry

        # Open the TIFF file and apply the clipping
        with rasterio.open(tiff_file) as src:
            clipped_data, clipped_transform = rasterio.mask.mask(src, clip_geometry, crop=True, nodata=-999)
            clipped_data = np.nan_to_num(clipped_data, nan=0)

            clipped_meta = src.meta.copy()
            clipped_meta.update({
                'height': clipped_data.shape[1],
                'width': clipped_data.shape[2],
                'transform': clipped_transform
            })

            # Write the clipped data to a new TIFF file
            with rasterio.open(output_filename, 'w', **clipped_meta) as dst:
                dst.write(clipped_data)

        print(f'Clipping completed. Clipped TIFF saved as: {output_filename}')

    except Exception as e:
        print(f"An error occurred during clipping: {e}")


def list_subfolders(path: str) -> list[str]:
    """
    Returns a list of all subfolders in the given folder path.
    
    :param path: Path to the parent folder.
    :return: List of paths to the subfolders.
    """
    subfolders = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            subfolders.append(os.path.join(root, dir))
        # Only get the immediate subdirectories, not recursive
        break
    return subfolders