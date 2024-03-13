import requests


def QR_code_datacube_data_insertion(api_key, database_name, collection_name, data):
    """
    Insert data into a collection in the DataCube database.

    :param api_key: The API key for authentication.
    :param database_name: The name of the database.
    :param collection_name: The name of the collection.
    :param data: The data to be inserted into the collection.
    :return: The response text from the server.
    """
    url = "https://datacube.uxlivinglab.online/db_api/crud/"

    payload = {
        "api_key": api_key,
        "db_name": database_name,
        "coll_name": collection_name,
        "operation": "insert",
        "data": data,
    }

    response = requests.post(url, json=payload)
    print(response)
    return response.text


def datacube_data_retrieval(api_key, database_name, collection_name, data):
    """
    Retrieve data from a collection in the DataCube database.

    :param api_key: The API key for authentication.
    :param database_name: The name of the database.
    :param collection_name: The name of the collection.
    :param data: Filters to apply when retrieving data.
    :param limit: The maximum number of documents to retrieve.
    :param offset: The number of documents to skip before starting to collect data.
    :param payment: Whether payment is required for accessing the data.
    :return: The response text from the server.
    """
    url = "https://datacube.uxlivinglab.online/db_api/get_data/"
    print(api_key)
    payload = {
        "api_key": api_key,
        "db_name": database_name,
        "coll_name": collection_name,
        "operation": "fetch",
        "filters": data,
        "limit": 1,
        "offset": 0
    }

    response = requests.post(url, json=payload)
    print(response.text)
    return response.text


def datacube_data_update(api_key, db_name, coll_name, query, update_data):
    """
    Update data in a collection in the DataCube database.

    :param api_key: The API key for authentication.
    :param db_name: The name of the database.
    :param coll_name: The name of the collection.
    :param query: The query to select the documents to update.
    :param update_data: The data to be updated in the selected documents.
    :return: The response text from the server.
    """
    url = "https://datacube.uxlivinglab.online/db_api/crud/"

    payload = {
        "api_key": api_key,
        "db_name": db_name,
        "coll_name": coll_name,
        "operation": "update",
        "query": query,
        "update_data": update_data,
    }

    response = requests.put(url, json=payload)
    print(response.text)
    return response.text

