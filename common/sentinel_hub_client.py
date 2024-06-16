"""
This module provides utility functions to interact with the Sentinel Hub API, 
including functions to retrieve authentication tokens and to fetch satellite data.

Functions:
- retrieve_sentinel_token(client_id: str, client_secret: str) -> str
- retrieve_sentinel_data(bbox: list[float], data_type: str, start_date: str, end_date: str, token: str) -> requests.Response

Possible data_type values:
- sentinel-1-grd
- sentinel-1-coh
- sentinel-2-l1c
- sentinel-2-l2a
- sentinel-3-olci
- sentinel-3-slstr
- sentinel-5p
- landsat-8-l1
- landsat-8-l2
- dem
- modis
"""

import os
from datetime import datetime

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def retrieve_sentinel_token(client_id: str, client_secret: str) -> str:
    """
    Retrieves an OAuth2 token from the Sentinel Hub API.

    Args:
        client_id (str): The client ID for the Sentinel Hub API.
        client_secret (str): The client secret for the Sentinel Hub API.

    Returns:
        str: The access token to be used for subsequent API requests.
    """
    try:
        # Create a session
        client = BackendApplicationClient(client_id = client_id)
        oauth = OAuth2Session(client = client)

        # Get token for the session
        token = oauth.fetch_token(
            token_url = 'https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token',
            client_id = client_id,
            client_secret = client_secret,
            include_client_id = True,
        )

        # Return the access token
        return token['access_token']

    except Exception as e:
        print(f"An error occurred while retrieving the token: {e}")
        raise


def retrieve_sentinel_data(
        bbox : list[float], 
        data_type : str, 
        start_date : str, 
        end_date : str, 
        token : str
    ) -> requests.Response :
    """
    Retrieves satellite data from the Sentinel Hub API.

    Args:
        bbox (list[float]): The bounding box coordinates [minx, miny, maxx, maxy].
        data_type (str): The type of data to retrieve. Possible values include:
            - sentinel-1-grd
            - sentinel-1-coh
            - sentinel-2-l1c
            - sentinel-2-l2a
            - sentinel-3-olci
            - sentinel-3-slstr
            - sentinel-5p
            - landsat-8-l1
            - landsat-8-l2
            - dem
            - modis
        start_date (str): The start date for the data retrieval period (format: YYYY-MM-DD).
        end_date (str): The end date for the data retrieval period (format: YYYY-MM-DD).
        token (str): The OAuth2 access token.

    Returns:
        requests.Response: The response object containing the retrieved data.
    """
    url = 'https://services.sentinel-hub.com/api/v1/process'
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "input": {
            "bounds": {
                "bbox": bbox
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": start_date,
                            "to": end_date
                        }
                    },
                    "type": data_type
                }
            ]
        },
        "output": {
            "responses": [
            {
                "identifier": "default",
                "format": {
                    "type": "image/tiff"
                }
            }
            ]
        },
        "evalscript" :  "//VERSION=3\n\nfunction setup() {\n  return {\n    " + 
                        "input: [\"B01\", \"B02\", \"B03\", \"B04\", \"B05\", \"B06\"],\n    " +
                        "output: { bands: 6 }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  " +
                        "// Return the input bands without modification\n  return [sample.B01, " +
                        "sample.B02, sample.B03, sample.B04, sample.B05, sample.B06];\n}"
    }

    print(f"Payload: {payload}")  # Print the payload to debug
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

    return response


def save_response_content(response: requests.Response, output_dir: str) -> None:
    """
    Save the content of the response to a file.

    Args:
        response (Response): The response object containing data.
        output_dir (str): Directory where the files will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    print(response.headers)
    # Extract the filename from the Content-Disposition header if present
    content_disposition = response.headers.get("Content-Disposition", "")
    if "attachment" in content_disposition:
        filename = content_disposition.split("filename=")[-1].strip("\"")
    else:
        # Generate a unique filename based on the current timestamp if no filename is provided
        filename = f"product_{datetime.now().strftime('%Y%m%d%H%M%S')}.tiff"

    file_path = os.path.join(output_dir, filename)
    with open(file_path, "wb") as file:
        file.write(response.content)
    
    print(f"Data saved to {file_path}")