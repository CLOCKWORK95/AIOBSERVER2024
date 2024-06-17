import glob
import os
import sys

PYTHONPATH = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024"
sys.path.append(PYTHONPATH)

from common.copernicus_open_access_hub_client import (download_sentinel_data,
                                                      get_access_token)
from common.file_operations import (clip_tiff_files, create_mosaic_from_folder,
                                    process_single_file)


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


def list_all_files(path: str) -> list[str]:
    """
    Returns a list of all files in the given folder path, including subfolders.
    
    :param path: Path to the parent folder.
    :return: List of paths to the files.
    """
    files_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list


def main():
    # Copernicus Open Access Hub credentials for token retrieval.
    CLIENT_ID = 'gianmarcobencivenni2@gmail.com'
    CLIENT_SECRET = 'Copernicus2024!'

    COLLECTION = "SENTINEL-2"
    PRODUCT_TYPE = "L2A"
    AOI = "POLYGON((6.34 47.41, 20.34 47.41, 20.34 36.07, 6.34 36.07, 6.34 47.41))"
    START_DATE = "2024-05-24"
    END_DATE = "2024-05-28"
    OUTPUT_DIRECTORY = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024\\data"
    UNZIPPED = "C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024\\unzipped"
    SHAPEFILE_PATH = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024\\shapefiles\\Italia\\italia.shp"
    TARGET_X_PIXEL_SIZE = 0.011131580833333335
    MOSAIC_OUTPUT_FILENAME = "mosaic.tif"

    # Retrieve the session token
    session_token = get_access_token(
        username=CLIENT_ID,
        password=CLIENT_SECRET,
    )

    # Download Satellite Data
    downloaded_files = download_sentinel_data(
        token = session_token,
        aoi = AOI,
        start_date = START_DATE,
        end_date = END_DATE,
        collection = COLLECTION,
        product_type = PRODUCT_TYPE,
        output_dir = OUTPUT_DIRECTORY,
        unzipped_dir = UNZIPPED,
        max_number = 1,
    )


    # TODO: Implement Some Custom Logic
    # custom_logic(...)

    # Clip the mosaic to the shapefile
    clip_tiff_files(
        output_filename=os.path.join(UNZIPPED, f"{downloaded_files[0]}_clipped.tif"),
        shapefile_path=SHAPEFILE_PATH,
        tiff_file=os.path.join(UNZIPPED, downloaded_files[0]),
    )


if __name__ == "__main__":
    main()
