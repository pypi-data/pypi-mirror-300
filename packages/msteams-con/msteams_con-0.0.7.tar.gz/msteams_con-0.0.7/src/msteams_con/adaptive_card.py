from json import dumps

from msteams_con.logger import Logger

LOGGER = Logger.get_logger(__name__)


class AdaptiveCard:
  """Constructs an Adaptive Card object."""

  @staticmethod
  def action_open_url(title: str, url: str) -> dict:
    """
    Constructs an 'Action.OpenUrl' object.

    Args:
      title (str): The title of the action.
      url (str): The URL to be opened when the action is triggered.

    Returns:
        dict: The 'Actio  n.OpenUrl' object with the specified title and URL.

    Reference:
      https://adaptivecards.io/explorer/Action.OpenUrl.html
    """
    LOGGER.debug(
      f"Creating 'Action.OpenUrl' object with title: {title} and url: {url}."
    )
    return {"type": "Action.OpenUrl", "title": title, "url": url}

  @staticmethod
  def action_set(actions: list) -> dict:
    """
    Constructs an 'ActionSet' object.

    Args:
      actions (list): The list of actions to be included in the 'ActionSet'.

    Returns:
      dict: The 'ActionSet' object with the specified actions.

    Note:
      Currently, only 'Action.OpenUrl' is supported. Other actions
      will be added in the future.

    Reference:
      https://adaptivecards.io/explorer/ActionSet.html
    """
    LOGGER.debug(f"Creating 'ActionSet' object with actions: {actions}.")
    return {"type": "ActionSet", "actions": actions}

  @staticmethod
  def image(url: str, **kwargs) -> dict:
    """
    Constructs an 'Image' object.

    Args:
      url (str): The URL of the image.
      **kwargs: Additional properties to be included in the 'Image' object.

    Returns:
      dict: The 'Image' object with the specified URL.

    Reference:
      More properties can be found at https://adaptivecards.io/explorer/Image.html

    Example:
      AdaptiveCard.image(url="https://example.com/image.jpg",
      width="100px", height="100px")
    """
    LOGGER.debug(f"Creating 'Image' object with url: {url}, kwargs: {kwargs}.")
    return {"type": "Image", "url": url, **kwargs}

  @staticmethod
  def text_block(text: str, **kwargs) -> dict:
    """
    Constructs a 'TextBlock' object.

    Args:
      text (str): The text to be included in the 'TextBlock'.
      **kwargs: Additional properties to be included in the 'TextBlock' object.

    Returns:
      dict: The 'TextBlock' object with the specified text.

    Reference:
      More properties can be found at https://adaptivecards.io/explorer/TextBlock.html

    Example:
      AdaptiveCard.text_block(text="Hello, World!", size="large", weight="bolder")
    """
    LOGGER.debug(f"Creating 'TextBlock' object with text: {text}, kwargs: {kwargs}.")
    return {"type": "TextBlock", "text": text, **kwargs}

  @staticmethod
  def column(item: list, **kwargs) -> dict:
    """
    Constructs a 'Column' object.

    Args:
      item (list): The items to be included in the 'Column'.
      **kwargs: Additional properties to be included in the 'Column' object.

    Returns:
      dict: The 'Column' object with the specified items.

    Reference:
      More properties can be found at https://adaptivecards.io/explorer/Column.html

    Example:
      AdaptiveCard.column(item=[AdaptiveCard.text_block("Hello")], width="auto")
    """
    LOGGER.debug(f"Creating 'Column' object with items: {item}, kwargs: {kwargs}.")
    return {"type": "Column", "items": item, **kwargs}

  @staticmethod
  def column_set(columns: list, **kwargs) -> dict:
    """
    Constructs a 'ColumnSet' object.

    Args:
      columns (list): The columns to be included in the 'ColumnSet'.
      **kwargs: Additional properties to be included in the 'ColumnSet' object.

    Returns:
      dict: The 'ColumnSet' object with the specified columns.

    Reference:
      More properties can be found at https://adaptivecards.io/explorer/ColumnSet.html

    Example:
      AdaptiveCard.column_set(
        columns=[AdaptiveCard.column([AdaptiveCard.text_block("Hello")])], style="good"
      )
    """
    LOGGER.debug(
      f"Creating 'ColumnSet' object with columns: {columns}, kwargs: {kwargs}."
    )
    return {"type": "ColumnSet", "columns": columns, **kwargs}

  @staticmethod
  def table(columns: list, rows: list, **kwargs) -> dict:
    """
    Constructs a 'Table' object.

    Args:
      columns (list): Defines the number of columns in the table, their sizes.
      rows (list): The rows to be included in the table.
      **kwargs: Additional properties to be included in the 'Table' object.

    Returns:
      dict: The 'Table' object with the specified columns and rows.

    Reference:
      More properties can be found at https://adaptivecards.io/explorer/Table.html
    """
    LOGGER.debug(
      f"Creating 'Table' object with columns: {columns}, "
      f"rows: {rows}, kwargs: {kwargs}."
    )
    return {"type": "Table", "columns": columns, "rows": rows, **kwargs}

  @staticmethod
  def table_row(cells: list, **kwargs) -> dict:
    """
    Constructs a 'TableRow' object.

    Args:
      cells (list): The cells to be included in the row.
      **kwargs: Additional properties to be included in the 'TableRow' object.

    Returns:
      dict: The 'TableRow' object with the specified cells.

    Example:
      AdaptiveCard.table_row(
        cells=[AdaptiveCard.table_cell(items=[AdaptiveCard.text_block("Hello")])]
      )
    """
    LOGGER.debug(f"Creating 'TableRow' object with cells: {cells}, kwargs: {kwargs}.")
    return {"type": "TableRow", "cells": cells, **kwargs}

  @staticmethod
  def table_cell(items: list, **kwargs) -> dict:
    """
    Constructs a 'TableCell' object.

    Args:
      items (list): The items to be included in the cell.
      **kwargs: Additional properties to be included in the 'TableCell' object.

    Returns:
      dict: The 'TableCell' object with the specified items.

    Reference:
      More properties can be found at https://adaptivecards.io/explorer/TableCell.html

    Example:
      AdaptiveCard.table_cell(
        items=[AdaptiveCard.text_block("Hello")], verticalContentAlignment="Center"
      )
    """
    LOGGER.debug(f"Creating 'TableCell' object with items: {items}, kwargs: {kwargs}.")
    return {"type": "TableCell", "items": items, **kwargs}

  @staticmethod
  def generate_adaptive_card(body: list) -> str:
    """
    Generates an Adaptive Card JSON payload.

    Args:
      body (list): The body of the Adaptive Card.

    Returns:
      str: The JSON payload of the Adaptive Card.
    """

    # Payload structure to send adaptive card
    # Reference: https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#send-adaptive-cards-using-an-incoming-webhook
    payload = {
      "type": "message",
      "attachments": [
        {
          "contentType": "application/vnd.microsoft.card.adaptive",
          "content": {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.6",
            "body": body,
          },
        }
      ],
    }
    return dumps(payload)
