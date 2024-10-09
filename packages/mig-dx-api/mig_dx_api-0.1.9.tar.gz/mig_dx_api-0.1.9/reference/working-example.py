#
# Basic Example
#
import httpx
import jwt
import datetime
import os
import io
import csv
from pathlib import Path

os.environ["DX_CONFIG_APP_ID"] = "8dcf69fd-8448-40a3-9e06-sdfsdfasd"
os.environ["DX_CONFIG_PRIVATE_KEY_PATH"] = "../.keys/privateKey.pem"


class BasicClient:
    base_url = "https://develop---mv-web-owjytbjtra-uk.a.run.app/api/v1/{}"

    def __init__(self, app_id, private_key_path):
        self.app_id = app_id
        self.private_key_path = private_key_path
        self.auth_token = self.create_auth_token()
        self.client_token = None
        self.session = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        self.installation_id = None

    def create_auth_token(self):
        # Read pivate key contents from .pem file
        private_key = open(self.private_key_path, "rb").read()

        issued_time = datetime.datetime.now(tz=datetime.timezone.utc)

        token = jwt.encode(
            {
                "iss": self.app_id,
                "aud": "movementconsole",
                "MovementAppId": self.app_id,
                "exp": issued_time + datetime.timedelta(hours=1),
                "iat": issued_time,
                "nbf": issued_time,
            },
            private_key,
            algorithm="RS256",
        )

        return token

    def whoami(self) -> dict:
        response = self.session.get(self.base_url.format("auth/me"))
        return response.json()

    def get_installations(self) -> dict:
        return self.session.get(self.base_url.format("apps/me/installations")).json()

    def get_client_token(self, installation_id: str) -> dict:
        resp = self.session.post(
            self.base_url.format("auth/clientToken"),
            json={
                "tokenType": "appInstallation",
                "installationId": installation_id,
                "permissions": [],
            },
        ).json()
        return resp

    def _parse_client_token(self, client_token: dict[str, str]):
        # parse datetime '2024-09-19T03:51:53.5738437Z
        client_token["expiresAt"] = datetime.datetime.fromisoformat(
            client_token["expiresAt"].replace("Z", "")[:-1] + "+00:00"
        )

        return client_token

    def authenticate_installation(self, installation_id: str):
        self.installation_id = installation_id
        self.client_token = self._parse_client_token(
            self.get_client_token(installation_id)
        )

    def _client_auth_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.client_token['token']}",
        }

    def _check_client_auth(self):
        if not self.installation_id:
            raise ValueError("Must authenticate installation first")
        if (
            datetime.datetime.now(datetime.timezone.utc)
            > self.client_token["expiresAt"]
        ):
            self.authenticate_installation(self.installation_id)

    def list_datasets(self):
        self._check_client_auth()
        return self.session.get(
            self.base_url.format("datasets"), headers=self._client_auth_headers()
        ).json()

    def create_dataset(self, name: str, description: str, schema: dict):
        self._check_client_auth()
        return self.session.post(
            self.base_url.format("datasets"),
            headers=self._client_auth_headers(),
            json={
                "name": name,
                "description": description,
                "schema": schema,
            },
        ).json()

    def get_upload_url(self, dataset_id: str, content_type: str):
        self._check_client_auth()
        return self.session.post(
            self.base_url.format(f"datasets/{dataset_id}/uploadUrl"),
            headers=self._client_auth_headers(),
            json={"contentType": content_type},
        ).json()

    def load_data_from_public_url(self, url: str):
        return self.session.post(
            self.base_url.format("datasets/:id/records:load?mode=replace"),
            headers=self._client_auth_headers(),
            json={"url": url},
        ).json()

    def upload_data_to_url(self, upload_url: str, data: list[dict]):
        _buffer = io.StringIO()
        writer = csv.DictWriter(_buffer, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        _buffer.seek(0)
        return self.session.put(
            upload_url, data=_buffer, headers={"Content-Type": "text/csv"}
        ).json()

    def upload_file_to_url(self, upload_url, file: Path):
        return self.session.put(upload_url, data=file.open("rb")).json()

    def get_download_url(self, dataset_id: str):
        self._check_client_auth()
        return self.session.post(
            self.base_url.format(f"datasets/{dataset_id}/records:retrieve"),
            headers=self._client_auth_headers(),
        ).json()

    def download_data_from_url(self, download_url: str):
        r = self.session.get(download_url)
        r.raise_for_status()
        with io.StringIO(r.text) as f:
            return list(csv.DictReader(f))


client = BasicClient(
    os.environ["DX_CONFIG_APP_ID"], os.environ["DX_CONFIG_PRIVATE_KEY_PATH"]
)

client.whoami()

# {'userId': 10001,
#  'workspaceId': 28,
#  'appId': '8dcf69fd-8448-40a3-9e06-asdfadsfasdf',
#  'userName': 'app-user-3ccf2473-9ceb-482a-82fa-asdfasdfasdf',
#  'email': None,
#  'dateTermsAccepted': None}

installations = client.get_installations()

# {'metadata': {'count': 1},
#  'data': [{'movementAppInstallationId': 26,
#    'movementAppId': '8dcf69fd-8448-40a3-9e06-asdfasdfasdf',
#    'workspaceId': 28,
#    'createdBy': {'userId': 10000,
#     'displayName': 'c9e78972-c036-41c3-a417-asdfasdfasdf',
#     'email': 'chris.goddard@movementinfrastructure.org'},
#    'dateCreated': '2024-09-18T16:01:00.917953',
#    'name': 'Test App'}]}

client.authenticate_installation(installations["data"][0]["movementAppInstallationId"])

client.list_datasets()

# {'metadata': {'count': 1},
#  'data': [{'datasetId': '1b81258c-066d-4944-a754-asdfasdfasdf',
#    'name': 'Example List A',
#    'description': 'An example list',
#    'dateCreated': '2024-09-18T16:11:28.914911',
#    'recordCount': 100,
#    'createdBy': {'userId': 10001,
#     'displayName': 'app-user-3ccf2473-9ceb-482a-82fa-a14d0e4ab546',
#     'email': ''},
#    'createdByWorkspace': {'workspaceId': 28,
#     'displayName': 'c9e78972-c036-41c3-a417-1b3805b5ca3f'},
#    'datasetTags': [],
#    'datasetSchema': {'datasetSchemaId': 34,
#     'properties': [{'type': 'string', 'required': True, 'name': 'van_id'},
#      {'type': 'string', 'required': True, 'name': 'first_name'},
#      {'type': 'string', 'required': True, 'name': 'last_name'},
#      {'type': 'string', 'required': True, 'name': 'phone_number'}],
#     'primaryKey': ['van_id']}}]}


{
    "metadata": {"count": 1},
    "data": [
        {
            "datasetId": "1b81258c-066d-4944-a754-asdfasdfasdf",
            "name": "Example List A",
            "description": "An example list",
            "dateCreated": "2024-09-18T16:11:28.914911",
            "recordCount": 100,
            "createdBy": {
                "userId": 10001,
                "displayName": "app-user-3ccf2473-9ceb-482a-82fa-a14d0e4ab546",
                "email": "",
            },
            "createdByWorkspace": {
                "workspaceId": 28,
                "displayName": "c9e78972-c036-41c3-a417-1b3805b5ca3f",
            },
            "datasetTags": [],
            "datasetSchema": {
                "datasetSchemaId": 34,
                "properties": [
                    {"type": "string", "required": True, "name": "van_id"},
                    {"type": "string", "required": True, "name": "first_name"},
                    {"type": "string", "required": True, "name": "last_name"},
                    {"type": "string", "required": True, "name": "phone_number"},
                ],
                "primaryKey": ["van_id"],
            },
        }
    ],
}
