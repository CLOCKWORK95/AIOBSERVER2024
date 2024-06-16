import os
import requests


def get_access_token(username: str, password: str) -> str:

    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }

    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data = data,
        )
        r.raise_for_status()

    except Exception as e:
        raise Exception(
            f"Access token creation failed. Reponse from the server was: {r.json()}"
        )

    return r.json()["access_token"]


def download_sentinel_data(
        token : str,
        aoi : str, 
        start_date : str, 
        end_date : str, 
        collection : str, 
        product_type : str, 
        output_dir : str
    ):
    # Define the URL and parameters for the request
    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    params = f"$filter=Collection/Name eq '{collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '{product_type}') and ContentDate/Start gt {start_date}T08:00:00.000Z and ContentDate/Start lt {end_date}T12:00:00.000Z"

    try:
        # Make the GET request to retrieve JSON response
        response = requests.get(f"{url}?{params}")
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        json_data = response.json()
        products = json_data.get('value', [])

        print(products)

        # Initialize a session with authentication
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {token}'})

        # Iterate over each product in the response
        for product in products:
            product_id = product['Id']
            product_name = product['Name']

            # Download the product using its ID
            url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
            response = session.get(url, allow_redirects=False)

            while response.status_code in (301, 302, 303, 307):
                url = response.headers['Location']
                response = session.get(url, allow_redirects=False)

            file = session.get(url, verify=False, allow_redirects=True)

            # Ensure the directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Specify the full path for the ZIP file using the product name
            output_path = os.path.join(output_dir, f'{product_name}.zip')

            with open(output_path, 'wb') as p:
                p.write(file.content)

            print(f"Downloaded ZIP file saved at: {output_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")