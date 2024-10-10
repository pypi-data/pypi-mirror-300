import time
import requests
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict
import logging
import httpx
import regex as re
import json

# Setup basic logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
json_pattern = re.compile(r'\{[^{}]*\}|\[[^\[\]]*\]')

@dataclass
class Message:
    content: str
    role: str
    type: str = "text"

    def __post_init__(self):
        if self.role not in ["user", "assistant"]:
            raise ValueError(f"Invalid role '{self.role}'. Role must be either 'user' or 'assistant'.")
        if self.type not in ["text", "other_allowed_type"]:
            raise ValueError(f"Invalid type '{self.type}'. Type must be 'text' or an allowed type.")

@dataclass
class MessageRequestPayload:
    organization_id: int = 0
    assistant_id: int = 0
    thread_id: Optional[int] = None
    model: Optional[str] = None
    instructions: Optional[str] = None
    additional_instructions: Optional[str] = None
    tool_choice: Optional[str] = "none"
    messages: List[Message] = field(default_factory=list)

    def to_dict(self) -> Dict:
        payload = {
            "organization_id": self.organization_id,
            "assistant_id": self.assistant_id,
            "thread_id": self.thread_id,
            "model": self.model,
            "instructions": self.instructions,
            "additional_instructions": self.additional_instructions,
            "tool_choice": self.tool_choice,
            "messages": [msg.__dict__ for msg in self.messages],
        }
        return {k: v for k, v in payload.items() if v is not None}

class StreamEvent:
    def __init__(self, event: str, status: Optional[str], is_response: bool, response: Optional[str], thread_id: int):
        self.event = event
        self.status = status
        self.is_response = is_response
        self.response = response
        self.thread_id = thread_id

    def __repr__(self):
        return f"<StreamEvent event={self.event} status={self.status} response={self.response} thread_id={self.thread_id}>"

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            event=data.get("event"),
            status=data.get("status"),
            is_response=data.get("isResponse", False),
            response=data.get("response"),
            thread_id=data.get("threadId")
        )

def is_valid_json(data):
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False

class FreddyApi:
    BASE_URLS = {
        "v1": "https://freddy-api.aitronos.com/v1"
    }

    def __init__(self, token: str, version: str = "v1"):
        if version not in self.BASE_URLS:
            raise ValueError(
                f"Unsupported API version: {version}. Supported versions are: {list(self.BASE_URLS.keys())}")

        self.token = token
        self.version = version
        self.base_url = self.BASE_URLS[version]
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.rate_limit_reached = False

    def create_stream(self, payload: "MessageRequestPayload", callback: callable) -> None:
        url = f"{self.base_url}/messages/run-stream"
        data = payload.to_dict()
        headers = {
            "Authorization": f"Bearer {self.token.strip()}",
            "Content-Type": "application/json"
        }

        try:
            timeout = httpx.Timeout(60.0)

            with httpx.Client(timeout=timeout) as client:
                with client.stream("POST", url, json=data, headers=headers) as response:
                    response.raise_for_status()

                    buffer = ""

                    for chunk in response.iter_text():
                        buffer += chunk
                        matches = list(re.finditer(json_pattern, buffer))

                        if matches:
                            for match in matches:
                                json_str = match.group()

                                try:
                                    json_data = json.loads(json_str)
                                    event = StreamEvent.from_json(json_data)
                                    callback(event)

                                except json.JSONDecodeError as e:
                                    log.error(f"Failed to decode JSON: {e}")

                            buffer = buffer[matches[-1].end():]

        except httpx.RequestError as e:
            log.error(f"Request to {url} failed. Error details: {e}")
            raise Exception(f"Network or connection error while making request to {url}. Details: {e}")

    def create_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
        if self.rate_limit_reached:
            log.error("Rate limit reached. Please try again later.")
            raise Exception("Rate limit reached, please try again later.")

        url = f"{self.base_url}/messages/run-create"
        data = payload.to_dict()

        try:
            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code == 200:
                self.rate_limit_reached = True
                return response.json()
            else:
                try:
                    error_message = response.json().get("error", response.text)
                except ValueError:
                    error_message = response.text
                log.error(f"API request to {url} failed with status {response.status_code}: {error_message}")
                raise Exception(f"API request failed with status {response.status_code}: {error_message}")

        except requests.RequestException as e:
            log.error(f"Error during the API request to {url}: {str(e)}")
            raise Exception(f"Network or server error occurred during API request. Details: {str(e)}")

    def check_run_status(self, run_key: str, thread_key: str, organization_id: int) -> str:
        url_status = f"{self.base_url}/messages/run-status"
        payload = {
            "organization_id": organization_id,
            "thread_key": thread_key,
            "run_key": run_key
        }

        try:
            response = requests.get(url_status, json=payload, headers=self.headers)

            if response.status_code == 200:
                response_data = response.json()
                run_status = response_data.get("runStatus", "unknown")
                return run_status
            else:
                log.error(f"Failed to retrieve run status from {url_status}. HTTP Status Code: {response.status_code}")
                return "error"

        except requests.RequestException as e:
            log.error(f"Error while checking run status at {url_status}: {e}")
            return "error"

    def get_run_response(self, organization_id: int, thread_key: str) -> Union[Dict, None]:
        url = f"{self.base_url}/messages/run-response"
        payload = {"organization_id": organization_id, "thread_key": thread_key}

        try:
            response = requests.get(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                error_message = response.json().get("error", response.text)
                raise Exception(f"Failed to get run response from {url}: {error_message}")
        except requests.RequestException as e:
            raise Exception(f"Error occurred while making request to {url}. Details: {e}")

    def execute_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
        url = f"{self.base_url}/messages/run-stream"

        # Convert the payload to a dictionary and add the "stream" key
        data = payload.to_dict()
        data.update({"stream": False})

        # Define the headers with authorization and content type
        headers = {
            "Authorization": f"Bearer {self.token.strip()}",
            "Content-Type": "application/json"
        }

        try:
            # Correct the method to POST and use the local 'headers' and 'data'
            response = requests.post(url, headers=headers, json=data)

            # Check if the response is successful
            if response.status_code == 200:
                return response.json()
            else:
                # Handle the error, parsing the response for detailed error information
                error_message = response.json().get("error", response.text)
                raise Exception(f"Failed to get response from {url}: {error_message}")

        except requests.RequestException as e:
            # Catch exceptions related to the HTTP request
            raise Exception(f"Error occurred while making request to {url}. Details: {e}")

