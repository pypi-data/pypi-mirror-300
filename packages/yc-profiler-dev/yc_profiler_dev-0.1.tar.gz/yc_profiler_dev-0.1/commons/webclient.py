import requests
from datetime import datetime
import socket
from log.ycrash_logger import ycrash_logger

"""
    yCrash Profiler: WebClient
    Uploads json request to the server url.
"""
def upload_json_data(contentType, apiKey, url, data):

    # Get the current time
    current_time = datetime.now()

    # Format the time as required
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    url = url+"?de="+ip_address+"?ts="+formatted_time+"&lang=py"
    # Set the Content-Type header to application/json
    headers = {'Content-Type': contentType,
               'Authorization': apiKey}
    ycrash_logger.debug(f"\n*****************************************************************************************")
    ycrash_logger.debug(f" \nHTTP post to  {url}  with headers {headers}")
    ycrash_logger.debug(f" DATA: ")
    ycrash_logger.debug(f" {data}")
    response = requests.post(url, data=data, headers=headers)
    ycrash_logger.debug(f"Response: {response}")
    if response.status_code == 200:
        ycrash_logger.debug('Data uploaded successfully!')
    else:
        ycrash_logger.debug('Error uploading data:', response.status_code)
    ycrash_logger.debug(f"*****************************************************************************************")
    # Send the POST request with JSON data

    # Check if the request was successful

