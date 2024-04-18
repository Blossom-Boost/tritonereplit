from requests import Session
from urllib.parse import urljoin
from requests.structures import CaseInsensitiveDict
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


class AgendorModule(Session):
    def __init__(self, base_url="https://api.agendor.com.br/"):
        super().__init__()
        self.base_url = base_url
        self.headers = CaseInsensitiveDict({
            "Authorization": "Token 905f0144-3cb2-453e-8279-9d4ceafd30c8"
        })

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        logger.info(joined_url)
        return super().request(method, joined_url, *args, **kwargs)

    def save_new_client(self, name: str, email: str, phone: str):
        return self.post(
            "/v3/people",
            json={
                "name": name,
                "email": email,
                "phone": phone,
            },
        )