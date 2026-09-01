from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()
conn_str = os.getenv("AZURE_CONN_STR")
container_name = os.getenv("AZURE_CONTAINER")

blob_service = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service.get_container_client(container_name)

print("Blobs en el contenedor:")
for blob in container_client.list_blobs():
    print(blob.name)
