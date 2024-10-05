# msteams-connector
Microsoft Teams connector for sending messages to Teams channels via webhooks.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3100/)
![MSTeams](https://img.shields.io/badge/Teams-6264A7?style=flat&logo=microsoft-teams&logoColor=white)
![PyPI](https://img.shields.io/pypi/v/msteams-con?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/msteams-con)

## Overview

msteams-connector is a Python-based tool to simplify the process of sending messages, adaptive card to Microsoft Teams channels via incoming webhooks. Whether you’re automating release notifications, error alerts, or general messages, this connector provides a seamless interface for working with Microsoft Teams.

## Prerequisites
### Get MSTeams Webhook

Before using this package, you will need to obtain an MS Teams webhook URL. Follow the instructions in the [Microsoft Teams Documentation](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet) to create a new incoming webhook in your MS Teams channel.

### Installation
```sh
pip install msteams-con
```


## Usage

### Example Code
```
from msteams_con import *
import os

hook_url = os.environ["MSTEAMS_WEBHOOK"]

msteams = MSTeamsConnector(hook_url)
payload = msteams.generate_text_payload("Hello, World!")
msteams.send_payload(payload)
```

### CLI

Send with our release card template
```
msteams-connector send_release_card --version <software-release-version> --hook_url <your_webhook_url>
```
Send with single text
```
msteams-connector send_text --text "hello world" --hook_url <your_webhook_url> 
```

## Developer Setup
If you want to contribute or modify the code, follow these steps to set up the project locally:
```
git clone https://github.com/cloud-bees/msteams-connector.git
cd msteams-connector
export PYTHONPATH=$(pwd)/src
export MSTEAMS_WEBHOOK=<your_webhook_url>
pip install -e ".[dev]"
```

### Running Tests

Pytest
```sh
pytest tests/msteams_con -v -s --log-cli-level=DEBUG
```
You also can run pytest in Vscode Debug, Note need to add WEBHOOK into .vscode/launch.json

ruff
```sh
ruff check --fix
ruff format
```