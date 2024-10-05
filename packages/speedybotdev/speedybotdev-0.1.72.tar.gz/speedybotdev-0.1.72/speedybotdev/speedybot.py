import json
from .speedycard import SpeedyCard
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
    def __init__(self, token: str):
        self.token = token
        self.middlewares = []
        self.top_middleware = None
        self.reject_middleware = None
        self.make_request = make_request
        self.API = {
            "messages": "https://webexapis.com/v1/messages",
            "attachments": "https://webexapis.com/v1/attachment/actions",
            "user": {
                "self": "https://webexapis.com/v1/people/me",
                "get_person_details": "https://webexapis.com/v1/people",
            },
            "rooms": "https://webexapis.com/v1/rooms",
            "room_details": "https://webexapis.com/v1/rooms",
            "webhooks": "https://webexapis.com/v1/webhooks",
        }
        self.fallbackText = "Your client does not support adaptive cards"

    # ... (Existing methods: set_token, card, send_card_to, send_to, reply)

    def _headers(self, content_type="application/json"):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": content_type
        }

    def _make_request(self, method, url, headers=None, data=None, params=None):
        if headers is None:
            headers = self._headers()
        response = self.make_request(method, url, headers=headers, data=data, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        return response

    def delete_message(self, msg_id: str) -> None:
        url = f"{self.API['messages']}/{msg_id}"
        self._make_request("DELETE", url)

    def delete_webhook(self, webhook_id: str) -> None:
        url = f"{self.API['webhooks']}/{webhook_id}"
        self._make_request("DELETE", url)

    def get_webhooks(self) -> List[Webhook]:
        url = self.API['webhooks']
        response = self._make_request("GET", url)
        return [Webhook(**item) for item in response.json().get("items", [])]

    def fetch_webhooks(self) -> List[Dict[str, str]]:
        webhooks = self.get_webhooks()
        return [{"id": w.id, "name": w.name, "resource": w.resource, "targetUrl": w.targetUrl} for w in webhooks]

    def setup(self, url: str, secret: Optional[str] = None) -> None:
        self.create_firehose(url, secret)
        self.create_attachment_actions_webhook(url, secret)

    def get_recent_rooms(self, limit: int = 100) -> List[Dict[str, str]]:
        url = f"{self.API['rooms']}?max={limit}&sortBy=lastactivity"
        response = self._make_request("GET", url)
        return [{"type": r["type"], "title": r["title"], "id": r["id"]} for r in response.json().get("items", [])]

    def create_attachment_actions_webhook(self, url: str, secret: Optional[str] = None) -> Webhook:
        payload = {
            "resource": "attachmentActions",
            "event": "created",
            "targetUrl": url,
            "name": f"{datetime.now().isoformat()}_attachmentActions",  # Use datetime.now().isoformat()
            "secret": secret
        }
        return self.create_webhook(payload)

    def create_firehose(self, url: str, secret: Optional[str] = None) -> Webhook:
        payload = {
            "resource": "messages",
            "event": "created",
            "targetUrl": url,
            "name": f"{datetime.now().isoformat()}_firehose",  # Use datetime.now().isoformat()
            "secret": secret
        }
        return self.create_webhook(payload)

    def create_webhook(self, payload: Dict[str, Any]) -> Webhook:
        url = self.API['webhooks']
        response = self._make_request("POST", url, data=json.dumps(payload))
        return Webhook(**response.json())

    def get_self(self) -> Dict[str, Any]:
        url = self.API['user']['self']
        response = self._make_request("GET", url)
        return response.json()

    def who_am_i(self) -> Dict[str, Any]:
        self_data = self.get_self()
        webhooks = self.get_webhooks()
        return {**self_data, "webhooks": webhooks}

    def peek_file(self, url: str) -> SpeedyFile:
        response = self._make_request("HEAD", url)
        return SpeedyFile(url, **self._extract_file_data(response), data=None)

    def get_file(self, url: str, response_type: Optional[str] = None) -> SpeedyFile:
        response = self._make_request("GET", url)
        file_data = self._extract_file_data(response)
        
        content_type = file_data['contentType']
        should_be_array_buffer = (not "json" in content_type and not "text" in content_type) or "image" in content_type

        if response_type == "arraybuffer" or should_be_array_buffer:
            data = response.content
        elif "json" in content_type:
            data = response.json()
        else:
            data = response.text

        return SpeedyFile(url, **file_data, data=data)

    def _extract_file_data(self, response):
        content_type = response.headers.get("content-type")
        content_disposition = response.headers.get("content-disposition")
        content_length = int(response.headers.get("content-length", 0))

        file_name = content_disposition.split(";")[1].split("=")[1].replace('"', '') if content_disposition else ""
        extension = file_name.split(".")[-1] if file_name else ""

        return {
            'contentType': content_type,
            'name': file_name,
            'extension': extension,
            'bytes': content_length
        }

    def send_to(self, destination: Union[str, Dict[str, str]], message: Union[str, SpeedyCard]) -> MessageResponse:
        if isinstance(message, SpeedyCard):
            return self.send_card_to(destination, message, self.fallbackText)

        target = self.resolve_destination(destination)

        payload = {**target, "markdown": message}
        response = self._make_request("POST", self.API['messages'], data=json.dumps(payload))
        return MessageResponse(**response.json())

    def _send(self, payload: Dict[str, Any]) -> MessageResponse:
        response = self._make_request("POST", self.API['messages'], data=json.dumps(payload))
        return MessageResponse(**response.json())

    def resolve_destination(self, destination: Union[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Resolves the destination based on the input format.
        
        - If the destination contains an '@' symbol, it's treated as an email address 
        and returned with the key 'toPersonEmail'.
        
        - If the destination doesn't contain an '@', it's assumed to be a roomId and 
        returned with the key 'roomId'.
        
        - If you need to send to a personId explicitly, pass a dictionary in the form 
        { 'toPersonId': 'somePersonId' } and it will be returned directly without modification.
        
        Args:
            destination (Union[str, Dict[str, str]]): Either an email, roomId, or a dictionary with 'toPersonId'.

        Returns:
            Dict[str, str]: A dictionary containing the appropriate destination key and value.
        """
        if isinstance(destination, str):
            if "@" in destination:
                # It's an email address, return with 'toPersonEmail' key
                return {"toPersonEmail": destination}
            else:
                # It's a roomId, return with 'roomId' key
                return {"roomId": destination}
        
        # Override: If a dictionary is passed, it's assumed to be in the correct format (e.g., { 'toPersonId': 'somePersonId' })
        return destination



# bot = SpeedyBot(token="your-token")

# @bot.on_text
# def handle_text(ctx, text: str):
#     print(f"Handling text: {text}")
#     return True

# @bot.on_file(lambda file: file.get("extension") == "pdf")
# def handle_file(ctx, file: Dict):
#     print(f"Handling file: {file['name']} with extension {file['extension']}")
#     return True

# @bot.on_card
# def handle_card(ctx, data: Dict, file: str):
#     file.capitalize
#     print(f"Handling card data: {data}")
#     return True
