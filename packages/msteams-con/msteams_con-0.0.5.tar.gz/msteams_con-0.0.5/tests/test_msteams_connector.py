import os
from http import HTTPStatus
from pathlib import Path

import pytest

from src import MSTeamsConnector
from src.card_templates import ReleaseCard


class TestMsteamConnector:
  MSTEAMS_WEBHOOK = os.getenv("MSTEAMS_WEBHOOK", None)
  msteams_connector = MSTeamsConnector(hook_url=MSTEAMS_WEBHOOK)

  @pytest.mark.skipif(MSTEAMS_WEBHOOK is None, reason="MSTEAMS_WEBHOOK is not set.")
  def test_send_message(self):
    text = self.msteams_connector.generate_text_payload("This is my message.")
    result = self.msteams_connector.send_payload(text)
    assert result == HTTPStatus.OK

  @pytest.mark.skipif(MSTEAMS_WEBHOOK is None, reason="MSTEAMS_WEBHOOK is not set.")
  def test_release_card(self):
    release_card = ReleaseCard(version="10.0.0")
    card = release_card.generate_release_card()
    result = self.msteams_connector.send_payload(payload=card)
    assert card is not None
    assert result == HTTPStatus.OK

    # Send the payload as a file
    with Path("release_card.json").open("w+") as file:
      file.write(card)
    result = self.msteams_connector.send_payload(file="release_card.json")
    assert card is not None
    assert result == HTTPStatus.OK
