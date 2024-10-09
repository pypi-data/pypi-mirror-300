import logging

import requests


def rest_api_client(url, method='get', return_type='json', **kwargs):
    """
    Makes a REST API request and returns the response in the specified format.

    Args:
        url (str): The URL of the API endpoint.
        method (str, optional): The HTTP method to use for the request (default is 'get').
        return_type (str, optional): The format to return the response in ('json' or 'object', default is 'json').
        **kwargs: Additional keyword arguments to pass to the `requests.request` method.

    Returns:
        dict or requests.Response or None: The response from the API in the specified format, or None if the request failed.

    Raises:
        requests.exceptions.RequestException: If the request fails due to network issues or invalid responses.
    """
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None  # Return None to indicate failure

    if return_type == 'json':
        return response.json()
    elif return_type == 'object':
        return response
