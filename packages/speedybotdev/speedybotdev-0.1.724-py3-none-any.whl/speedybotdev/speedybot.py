import json
import urllib.request
from typing import NamedTuple, List, Dict, Any, Union, Optional
from datetime import datetime


class MessageResponse(NamedTuple):
    id: str
    roomId: str
    toPersonEmail: str
    roomType: str
    text: str
    personId: str
    personEmail: str
    markdown: str
    html: str
    created: str


class SpeedyFile(NamedTuple):
    url: str
    name: str
    extension: str
    contentType: str
    bytes: int
    data: Any


class Webhook(NamedTuple):
    id: str
    name: str
    resource: str
    event: str
    targetUrl: str
    created: str
    secret: Optional[str]


class SpeedyBot:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.API = {
            "messages": "https://webexapis.com/v1/messages",
            "webhooks": "https://webexapis.com/v1/webhooks",
            "user": {
                "self": "https://webexapis.com/v1/people/me"
            },
            "rooms": "https://webexapis.com/v1/rooms"
        }
        self.fallbackText = "Your client does not support adaptive cards"

    def set_token(self, token: str):
        """Set the token value."""
        self.token = token

    def get_token(self) -> Optional[str]:
        """Get the current token value."""
        return self.token

    def has_token(self) -> bool:
        """Check if a token is set."""
        return self.token is not None

    def _make_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None) -> Any:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        request = urllib.request.Request(url, headers=headers, method=method)

        if data:
            request.data = json.dumps(data).encode()

        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())

    def delete_message(self, msg_id: str) -> None:
        url = f"{self.API['messages']}/{msg_id}"
        self._make_request(url, method="DELETE")

    def delete_webhook(self, webhook_id: str) -> None:
        url = f"{self.API['webhooks']}/{webhook_id}"
        self._make_request(url, method="DELETE")

    def get_webhooks(self) -> List[Webhook]:
        url = self.API['webhooks']
        response = self._make_request(url)
        return [Webhook(**item) for item in response.get("items", [])]

    def fetch_webhooks(self) -> List[Dict[str, str]]:
        webhooks = self.get_webhooks()
        return [{"id": w.id, "name": w.name, "resource": w.resource, "targetUrl": w.targetUrl} for w in webhooks]

    def setup(self, url: str, secret: Optional[str] = None) -> None:
        self.create_firehose(url, secret)
        self.create_attachment_actions_webhook(url, secret)

    def get_recent_rooms(self, limit: int = 100) -> List[Dict[str, str]]:
        url = f"{self.API['rooms']}?max={limit}&sortBy=lastactivity"
        response = self._make_request(url)
        return [{"type": r["type"], "title": r["title"], "id": r["id"]} for r in response.get("items", [])]

    def create_attachment_actions_webhook(self, url: str, secret: Optional[str] = None) -> Webhook:
        payload = {
            "resource": "attachmentActions",
            "event": "created",
            "targetUrl": url,
            "name": f"{datetime.now().isoformat()}_attachmentActions",
            "secret": secret
        }
        return self.create_webhook(payload)

    def create_firehose(self, url: str, secret: Optional[str] = None) -> Webhook:
        payload = {
            "resource": "messages",
            "event": "created",
            "targetUrl": url,
            "name": f"{datetime.now().isoformat()}_firehose",
            "secret": secret
        }
        return self.create_webhook(payload)

    def create_webhook(self, payload: Dict[str, Any]) -> Webhook:
        url = self.API['webhooks']
        response = self._make_request(url, method="POST", data=payload)
        return Webhook(**response)

    def get_self(self) -> Dict[str, Any]:
        url = self.API['user']['self']
        response = self._make_request(url)
        return response

    def who_am_i(self) -> Dict[str, Any]:
        self_data = self.get_self()
        webhooks = self.get_webhooks()
        return {**self_data, "webhooks": webhooks}

    def peek_file(self, url: str) -> SpeedyFile:
        response = self._make_request(url, method="HEAD")
        return SpeedyFile(url, **self._extract_file_data(response), data=None)

    def get_file(self, url: str, response_type: Optional[str] = None) -> SpeedyFile:
        response = self._make_request(url)
        file_data = self._extract_file_data(response)

        content_type = file_data['contentType']
        should_be_array_buffer = (not "json" in content_type and not "text" in content_type) or "image" in content_type

        if response_type == "arraybuffer" or should_be_array_buffer:
            data = response.read()  # Raw bytes
        elif "json" in content_type:
            data = response
        else:
            data = response.text

        return SpeedyFile(url, **file_data, data=data)

    def _extract_file_data(self, response) -> Dict[str, Any]:
        content_type = response.get("contentType", "")
        content_disposition = response.get("content-disposition", "")
        content_length = int(response.get("content-length", 0))

        file_name = content_disposition.split(";")[1].split("=")[1].replace('"', '') if content_disposition else ""
        extension = file_name.split(".")[-1] if file_name else ""

        return {
            'contentType': content_type,
            'name': file_name,
            'extension': extension,
            'bytes': content_length
        }

    def send_to(self, destination: Union[str, Dict[str, str]], message: Union[str, SpeedyFile]) -> MessageResponse:
        target = self.resolve_destination(destination)

        payload = {**target, "markdown": message}
        response = self._make_request(self.API['messages'], method="POST", data=payload)
        return MessageResponse(**response)

    def resolve_destination(self, destination: Union[str, Dict[str, str]]) -> Dict[str, str]:
        if isinstance(destination, str):
            if "@" in destination:
                return {"toPersonEmail": destination}
            else:
                return {"roomId": destination}
        return destination
