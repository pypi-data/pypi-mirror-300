import requests
import os
import time
import zipfile

VALYU_INTERMEDIARY_ENDPOINT = "http://ec2-35-177-58-41.eu-west-2.compute.amazonaws.com:3000"

def load_dataset(api_key, dataset_id, save_path='downloads/archive.zip', node_id='valyu'):
    try:
        """Retrieve and download data from the intermediary service to a specified file path."""
        
        print(f"Fetching dataset {dataset_id}...")

        if node_id == 'valyu':
            intermediary_url = VALYU_INTERMEDIARY_ENDPOINT
        else:
            raise ValueError('Invalid node ID')

        time.sleep(2)
        headers = {'x-api-key': api_key}
        body = {
            "datasetId": dataset_id
        }
    
        # Fetch the presigned URL
        response = requests.post(f"{intermediary_url}/fetchData", headers=headers, json=body)
        response.raise_for_status()

        data = response.json()
        presigned_url = data['presignedURL']
    
        # Download the data
        response = requests.get(presigned_url)

        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
    
            # Unzip the file into a folder named after the zip file without its extension
            unzip_dir = os.path.join(os.path.dirname(save_path), os.path.basename(save_path).replace('.zip', ''))
            os.makedirs(unzip_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)

            print(f"Dataset downloaded successfully into {unzip_dir}.")
    
        else:
            raise Exception("Failed to download the data")
    except Exception as e:
        raise Exception(f"Error occurred: {e}")