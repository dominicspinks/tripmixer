from django.conf import settings
from django.core.files.storage import Storage
import requests
import jwt

class StoreBytesStorage(Storage):
    """
    Custom storage class for Storebytes API.
    """
    def __init__(self, name=None):
        self.api_url = settings.STOREBYTES_API_URL
        self.api_key = settings.STOREBYTES_API_KEY
        self.bucket_name = settings.STOREBYTES_BUCKET_NAME
        self.token = None
        self.token_expiry = 0

    def _get_token(self):
        """
        Fetches a valid token from the Storebytes API.
        """
        import time
        current_time = time.time()
        if self.token and current_time < self.token_expiry:
            return self.token

        verify_ssl = not settings.DEBUG

        response = requests.post(
            f"{self.api_url}/api/auth/token",
            json=self.api_key,
            verify=verify_ssl
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data["token"]
            self.token_expiry = jwt.decode(self.token, options={"verify_signature": False}).get("exp", current_time)
            return self.token
        else:
            raise Exception(f"Failed to retrieve Storebytes token: {response.json()}")

    def _open(self, name, mode='rb'):
        return None

    def _save(self, name, content):
        """
        Saves the file to Storebytes and returns the URL.
        """
        token = self._get_token()
        verify_ssl = not settings.DEBUG

        if hasattr(content, 'field') and hasattr(content.field, 'upload_to'):
            name = content.field.upload_to(content.instance, name)

        content_type = content.content_type if hasattr(content, 'content_type') else 'application/octet-stream'

        response = requests.post(
            f"{self.api_url}/api/files/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (name, content, content_type)},
            data={"bucketName": self.bucket_name},
            verify=verify_ssl
        )
        if response.status_code == 200:
            return response.json().get("url")
        else:
            raise Exception(f"Failed to upload file to Storebytes: {response.json()}")

    def exists(self, name):
        """
        Always returns False to allow overwriting files.
        """
        return False

    def save(self, name, content, max_length=None):
        """
        Overrides the save method to handle Storebytes storage.
        """
        return self._save(name, content)

    def url(self, name):
        """
        Returns the URL to access the file.
        """
        return f"{self.api_url}/api/files/{name}"
