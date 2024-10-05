import json
from http import HTTPStatus
from pathlib import Path

import requests

from msteams_con import Logger
from msteams_con.errors import MSTeamsWebhookError

LOGGER = Logger.get_logger(__name__)


class MSTeamsConnector:
  """Microsoft Teams connector class."""

  def __init__(self, hook_url: str):
    self.hook_url = hook_url

  def generate_text_payload(self, text: str) -> str:
    """
    Generate a JSON payload with the provided text.

    Args:
      text (str): The text to be included in the payload.

    Returns:
      str: The JSON payload as a string.
    """
    payload = {"text": text}
    LOGGER.info(f"Generated payload: {payload}")
    return json.dumps(payload)

  def send_payload(
    self, payload: str | None = None, file: Path | None = None, timeout=60
  ) -> HTTPStatus:
    """
    Sends a payload or file content to Microsoft Teams webhook.

    Args:
      payload (str, optional): The payload to send as a string. Defaults to None.
      file (Path, optional): The path to the file to send. Defaults to None.
      timeout (int): The timeout for the HTTP request in seconds. Defaults to 60.

    Note:
      Either payload or file content must be provided.

    Returns:
      HTTPStatus: The HTTP status code of the response.

    Raises:
      ValueError: If neither payload nor file is provided.
      TeamsWebhookError: If the HTTP response status code is not OK.
    """

    headers = {"Content-Type": "application/json"}

    if file:
      with Path(file).open() as f:
        data = f.read().encode("utf-8")
    elif payload:
      data = payload.encode("utf-8")
    else:
      raise ValueError("Either payload or file must be provided.")

    response = requests.post(
      self.hook_url,
      data=data,
      headers=headers,
      timeout=timeout,
    )
    LOGGER.info(f"Sending data to Microsoft Teams: {data}")

    if response.status_code != HTTPStatus.OK:
      raise MSTeamsWebhookError(response.reason)
    return HTTPStatus.OK
