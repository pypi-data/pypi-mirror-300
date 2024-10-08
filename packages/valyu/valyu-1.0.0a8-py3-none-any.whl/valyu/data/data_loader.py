from io import BytesIO
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

        # Download the zip file
        try:
            response = requests.get(presigned_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the zip file: {e}")
            return False
        
        # Extract the contents
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.filename.startswith('__MACOSX'):
                    zip_ref.extract(file_info, save_path)
        
        # Remove any empty directories
        for root, dirs, files in os.walk(save_path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
        
        print(f"Data downloaded successfully to {save_path}.")
    
    except Exception as e:
        raise Exception(f"Error occurred: {e}")