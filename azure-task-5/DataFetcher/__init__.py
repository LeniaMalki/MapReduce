from azure.storage.blob import BlobServiceClient

STORAGEACCOUNTURL = 'https://azuretask5app.blob.core.windows.net'
STORAGEACCOUNTKEY = 'ZAyXGQeAQ0ly6wIuYrKuflCwNI3SrjQx1T3pxeiLHXYfFqPgKtjVq7ZzuF4wkKitz6MHHrsf0Vpl+AStH2MVuQ=='
CONTAINERNAME = 'lea-container'


def main(name : str) -> dict:
    # Create the BlobServiceClient object
    blob_serv_instance = BlobServiceClient(STORAGEACCOUNTURL, STORAGEACCOUNTKEY)
    container = blob_serv_instance.get_container_client('lea-container')
    blob_list = container.list_blobs()
    files = {}

    for blob in blob_list:
        blob_cli_instance = blob_serv_instance.get_blob_client(CONTAINERNAME, blob.name, snapshot=None)
        blob_data = blob_cli_instance.download_blob()

        data = blob_data.readall().decode("utf-8")
        splitted_data = []
        counter = 0
        for line in data.splitlines():
            splitted_data.append({counter: line})
            counter += 1
            files[blob.name] = splitted_data

    return files