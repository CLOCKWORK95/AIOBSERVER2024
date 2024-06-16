import sys

PYTHONPATH = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024"
sys.path.append(PYTHONPATH)

from common.copernicus_open_access_hub_client import download_sentinel_data, get_access_token
from common.sentinel_hub_client import (retrieve_sentinel_data,
                                        retrieve_sentinel_token,
                                        save_response_content)


def main():
    
    # Copernicus Open Access Hub credentials for token retrieval.
    CLIENT_ID = 'gianmarcobencivenni2@gmail.com'
    CLIENT_SECRET = 'Copernicus2024!'

    COLLECTION = "SENTINEL-3"
    PRODUCT_TYPE = "LST"
    AOI = "POLYGON((6.34 47.41, 20.34 47.41, 20.34 36.07, 6.34 36.07, 6.34 47.41))"
    START_DATE = "2024-05-24"
    END_DATE = "2024-05-24"
    OUTPUT_DIRECTORY = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024\\data"


    # Retrieve the session token
    session_token = get_access_token(
        username = CLIENT_ID,
        password = CLIENT_SECRET,
    )

    download_sentinel_data(
        token = session_token,
        aoi = AOI,
        start_date = START_DATE,
        end_date = END_DATE,
        collection = COLLECTION,
        product_type = PRODUCT_TYPE,
        output_dir = OUTPUT_DIRECTORY,
    )



if __name__ == "__main__":
    main()
