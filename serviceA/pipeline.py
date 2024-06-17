import os
import sys

PYTHONPATH = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024"
sys.path.append(PYTHONPATH)

from common.copernicus_open_access_hub_client import (download_sentinel_data,
                                                      get_access_token)
from common.file_operations import clip_tiff_files


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
        output_filename = os.path.join(UNZIPPED, f"{downloaded_files[0]}_clipped.tif"),
        shapefile_path = SHAPEFILE_PATH,
        tiff_file = os.path.join(UNZIPPED, downloaded_files[0]),
    )


if __name__ == "__main__":
    main()
