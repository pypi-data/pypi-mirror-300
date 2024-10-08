import os
import base64
import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from pprint import pprint


def upload_to_platform(params: dict):
    """
    Upload an image to the platform using GraphQL API. The function handles both the file upload process and assigns the uploaded image to a project.

    Parameters:
    - params (dict): Dictionary containing the following keys:
        - team_name (str): Team identifier for authentication.
        - access_key (str): API access key for authentication.
        - project_id (str): The project ID to which the uploaded data will be assigned.
        - binary_data (bytes): The binary data of the image to be uploaded.
        - file_type (str): The file type of the image (e.g., 'jpg', 'png').
        - file_size (int): The size of the image file in bytes.
        - data_key (str): The unique identifier for the image.
        - dataset_name (str): The dataset name to which the image is being uploaded.

    Raises:
    - Exception: If an unexpected error occurs during the upload or project assignment process.
    """

    url = "https://api.superb-ai.com/v3/graphql"

    auth_value = f"{params['team_name']}:{params['access_key']}"
    encoded_auth = base64.b64encode(auth_value.encode("utf-8")).decode("utf-8")

    headers = {
        "X-Api-Key": params["access_key"],
        "X-Tenant-Id": params["team_name"],
        "Authorization": f"Basic {encoded_auth}",
    }

    transport = RequestsHTTPTransport(
        url=url,
        use_json=True,
        headers=headers,
    )

    graphql_client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    query_upload = gql(
        """
        mutation($type: String!, $fileInfo: JSONObject!) {
        createDatum(type: $type, fileInfo: $fileInfo) {
            id
            uploadUrl
            dataKey
        }
        }
        """
    )

    params_upload = {
        "type": "img-presigned-url",
        "fileInfo": {
            "key": params["data_key"],
            "group": params["dataset_name"],
            "file_name": params["data_key"],
            "file_size": params["file_size"],
        },
    }

    try:
        response_upload = graphql_client.execute(
            query_upload, variable_values=params_upload
        )

        presigned_url = response_upload["createDatum"]["uploadUrl"]["url"][
            "image_url"
        ]
        data_id = response_upload["createDatum"]["id"]

        print("data id:", data_id)

        headers_upload = {
            "Content-Type": f"image/{params['file_type']}",
            "Content-Length": str(params["file_size"]),
        }

        response_image_upload = requests.put(
            presigned_url, data=params["binary_data"], headers=headers_upload
        )

        if response_image_upload.status_code == 200:
            print("image uploaded successfully.", response_image_upload)

            query_label = gql(
                """
                mutation (
                $projectId: String!,
                $dataId: String!
                ) {
                createLabel(projectId: $projectId, dataId:$dataId)
                }
                """
            )

            params = {
                "projectId": str(params["project_id"]),
                "dataId": str(data_id),
            }

            response_label = graphql_client.execute(
                query_label, variable_values=params
            )

            print(response_label)
        else:
            print("image upload failed:", response_image_upload)

    except Exception as e:
        print(f"An error occurred: {e}")
