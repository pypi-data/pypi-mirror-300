from pathlib import Path

from msteams_con import AdaptiveCard


class ReleaseCard(AdaptiveCard):
  """Represents a release card for MSTeams Connector."""

  def __init__(self, version: str):
    self.version = version

  def generate_release_card(self, save_file: Path | None = None) -> str:
    """
    Generates the body of the release card.

    Args:
      save_file (Path | None): Optional. The file path to save the
      generated card payload.

    Returns:
      str: The generated body of the release card.
    """
    image_url = "https://www.jenkins.io/images/logos/chatterbox/chatterbox.png"
    changelog_url = "https://github.com/cloud-bees/msteams-connector/CHANGELOG.md"

    image = [
      self.image(
        image_url,
        width="200px",
      )
    ]
    text = [
      self.text_block(
        f"MSTeams Connector {self.version} Release 🎉",
        size="Large",
        weight="Bolder",
        wrap="true",
        horizontalAlignment="left",
      ),
      # Double new line character to create a new line
      self.text_block(
        "Dear all,\n\n"
        "We are pleased to announce the release of MSTeams Connector"
        f"version **{self.version}**.\n\n"
        "Please find the changelog below for more details.\n\n"
        "Thank you for your continued support and feedback.\n\n"
        "Best regards,\n\n"
        "Cloud Bees Team",
        weight="Default",
        wrap="true",
        horizontalAlignment="left",
      ),
    ]
    cells = [
      self.table_cell(image, verticalContentAlignment="Center"),
      self.table_cell(text),
    ]

    actions = [
      self.action_open_url(
        title="CHANGELOG",
        url=changelog_url,
      )
    ]
    rows = [self.table_row(cells)]
    columns = [{"width": 1}, {"width": 2}]
    body = [
      self.table(columns, rows, gridStyle="good"),
      self.action_set(actions),
    ]

    adaptive_card_payload = self.generate_adaptive_card(body)
    if save_file:
      with Path(save_file).open("w+") as f:
        f.write(adaptive_card_payload)

    return adaptive_card_payload
