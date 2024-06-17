import sys

PYTHONPATH = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024"
sys.path.append(PYTHONPATH)

from common.sentinel_hub_client import (retrieve_sentinel_data,
                                        retrieve_sentinel_token,
                                        save_response_content)


def main():

    # Sentinel Hub credentials for token retrieval.
    CLIENT_ID = '94a94646-e13c-4aa8-98cd-f93809bd0241'
    CLIENT_SECRET = 'xlhON2qO5mrRdIhm0VfpIaV1pPZ16rUn'

    # Define a bounding box to fetch third-party satellite data.
    DATA_TYPE = "sentinel-2-l2a"
    BBOX =  [ 12.212447, 41.72541, 12.659915, 42.048477 ]
    START_DATE = "2024-05-24T00:00:00Z"
    END_DATE = "2024-06-10T23:59:59Z"
    OUTPUT_DIR = f"C:\\Users\\gimbo\\python_workspace\\AIOBSERVER2024\\data"


    # Retrieve the session token
    session_token = retrieve_sentinel_token(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
    )

    # Retrieve the satellite data
    response = retrieve_sentinel_data(
        bbox = BBOX,
        data_type = DATA_TYPE,
        start_date = START_DATE,
        end_date = END_DATE,
        token = session_token,
    )


    # Handle the response
    if response.status_code == 200:
        print("Data retrieval successful!")
        save_response_content(response, OUTPUT_DIR)
    else:
        print(f"Data retrieval failed with status code {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()
