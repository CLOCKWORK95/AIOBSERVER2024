import os
import requests
import zipfile


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
        token: str,
        aoi: str, 
        start_date: str, 
        end_date: str, 
        collection: str, 
        product_type: str, 
        output_dir: str,
        unzipped_dir : str,
        max_number: int,
    ) -> list[str]:
    """
    Downloads Sentinel data for a specified area of interest (AOI), date range, collection, and product type.
    The data is saved in the specified output directory and returns a list of directories containing the extracted data.

    Args:
        token (str): Authorization token for accessing Sentinel data.
        aoi (str): Area of interest in WKT format.
        start_date (str): Start date for data retrieval in ISO 8601 format.
        end_date (str): End date for data retrieval in ISO 8601 format.
        collection (str): Data collection name (e.g., SENTINEL-2).
        product_type (str): Product type (e.g., Level-2A).
        output_dir (str): Directory to save the downloaded data.
        max_number (int): Maximum number of products to download.

    Returns:
        List[str]: List of paths to the directories containing the extracted data.
    """
    
    # Define the URL and parameters for the request
    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    params = f"$filter=Collection/Name eq '{collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '{product_type}') and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T23:59:59.999Z"

    downloaded_directories = []

    try:
        # Make the GET request to retrieve JSON response
        response = requests.get(f"{url}?{params}")
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        json_data = response.json()
        products = json_data.get('value', [])

        # Limit the number of products to download
        products = products[:max_number]

        # Initialize a session with authentication
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {token}'})

        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)

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

            # Specify the full path for the ZIP file using the product name
            zip_path = os.path.join(output_dir, f'{product_name}.zip')

            with open(zip_path, 'wb') as p:
                p.write(file.content)

            print(f"Downloaded ZIP file saved at: {zip_path}")

            # Extract the ZIP file
            extract_path = os.path.join(unzipped_dir, product_name)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            # Verifica del contenuto della cartella estratta
            extracted_files = os.listdir(extract_path)
            print(f"Files in {extract_path}: {extracted_files}")

            # Add the path to the extracted directory
            downloaded_directories.append(extract_path)

            # Remove the ZIP file
            os.remove(zip_path)

            print(f"Extracted and removed ZIP file: {zip_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    # Return the sorted list of directories
    return downloaded_directories
