# msteams-connector
A Python connector for sending messages to Microsoft Teams channels via webhooks.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3100/)
![MSTeams](https://img.shields.io/badge/Teams-6264A7?style=flat&logo=microsoft-teams&logoColor=white)
[![PyPI](https://img.shields.io/pypi/v/msteams-con?label=pypi%20package)](https://pypi.org/project/msteams-con)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/msteams-con)](https://pypi.org/project/msteams-con)
[![GitHub CI](https://github.com/cloud-bees/msteams-connector/actions/workflows/main.yaml/badge.svg)](https://github.com/cloud-bees/msteams-connector/actions/workflows/main.yaml)
[![codecov](https://codecov.io/github/cloud-bees/msteams-connector/graph/badge.svg?token=77ZAL5T9Q2)](https://codecov.io/github/cloud-bees/msteams-connector)

## Overview

msteams-connector is a Python-based library to simplify the process of sending messages, adaptive cards to Microsoft Teams channels via incoming webhooks. Whether you need to automate notifications, release announcements, or send custom messages, this connector provides a seamless interface for working with Microsoft Teams.

## Prerequisites

### Get MSTeams Webhook

Before using this package, you will need to obtain an MS Teams webhook URL. Follow the instructions in the [Microsoft Teams Documentation](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet) to create a new incoming webhook in your MS Teams channel.

## Installation

Install the library via pip:
```sh
pip install msteams_con
```


## Usage

### Example Code

Here is an example of how to send a basic text message to an MS Teams channel using this library:
```python
from msteams_con import *
import os

hook_url = os.environ["MSTEAMS_WEBHOOK"]

msteams = MSTeamsConnector(hook_url)
payload = msteams.generate_text_payload("Hello World!")
msteams.send_payload(payload)
```

### CLI

The package also provides CLI commands for sending messages to MS Teams.

**Send with our release card template**
  ```sh
  msteams-connector send_release_card --version <software-release-version> --hook_url <your_webhook_url>
  ```
**Send a simple text message**
  ```sh
  msteams-connector send_text --text "Hello World!" --hook_url <your_webhook_url> 
  ```

### Video Instructions

[![Watch the video](assets/Demo.gif)](assets/Demo.gif)

## Developer Setup
If you want to contribute or modify the code, follow these steps to set up the project locally:
```sh
git clone https://github.com/cloud-bees/msteams-connector.git
cd msteams-connector
export PYTHONPATH=$(pwd)
export MSTEAMS_WEBHOOK=<your_webhook_url>
pip install -e ".[dev]"
```
This installs the package in editable mode along with all development dependencies.

## Running Tests

To run tests and check code quality, use the following commands:

**Pytest**

Run the unit tests using pytest:
  ```sh
  pytest tests -v -s --log-cli-level=DEBUG
  ```
You can also run pytest in Visual Studio Code Debug mode. Make sure to add the WEBHOOK environment variable in .vscode/launch.json and set the Python interpreter correctly.

**Ruff for Linting and Formatting**

To check and autofix formatting issues, use ruff:
  ```sh
  ruff check --fix
  ruff format
  ```

## Contribution Guidelines

If you want to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a clear description of the changes.