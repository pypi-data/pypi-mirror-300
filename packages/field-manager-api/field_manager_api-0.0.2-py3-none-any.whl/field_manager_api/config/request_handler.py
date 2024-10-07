import requests


def get_request_handler(url: str, headers: dict):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # print("Request successful!")
            return (
                response.json()
            )  # or response.text, based on the API's response format
        elif response.status_code == 401:
            print("Authorization failed: Token may need to be refreshed or changed.")
            raise PermissionError("Token authorization failed (401 Unauthorized).")
        else:
            print(f"Request failed with status code: {response.status_code}")
            response.raise_for_status()  # Raise an exception for error status codes

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise requests.exceptions.HTTPError("An HTTP error occurred.") from http_err
    except requests.exceptions.ConnectionError as conn_err:
        print("Connection error occurred. Please check the URL or network connection.")
        raise ConnectionError("Failed to connect to the server.") from conn_err
    except requests.exceptions.Timeout as timeout_err:
        print("Request timed out. Try again later.")
        raise TimeoutError("The request timed out.") from timeout_err
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        raise RuntimeError("An unspecified request error occurred.") from req_err
