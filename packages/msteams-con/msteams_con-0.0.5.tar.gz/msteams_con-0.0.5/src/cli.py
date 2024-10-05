"""Microsoft Teams Connector Command Line Interface."""

import fire

from card_templates import ReleaseCard
from msteams_connector import MSTeamsConnector


class Pipeline:
  def __init__(self, hook_url: str | None = None, version: str | None = None):
    self.msteams_connector = MSTeamsConnector(hook_url)
    self.release_card = ReleaseCard(version)

  def send_release_card(self):
    self.msteams_connector.send_payload(self.release_card.generate_release_card())

  def send_text(
    self,
    text: str | None = None,
  ):
    self.msteams_connector.send_payload(
      self.msteams_connector.generate_text_payload(text)
    )


def main():
  fire.Fire(Pipeline)


if __name__ == "__main__":
  main()
