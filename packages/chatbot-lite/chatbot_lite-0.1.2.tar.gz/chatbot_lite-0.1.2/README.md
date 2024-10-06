# chatbot-lite

A Python-based chatbot designed to provide conversational responses.

## Table of Contents
1. [Prerequisites](#prerequisites)
   - [Install Python](#install-python)
   - [Install PIP](#install-pip)
2. [Installation](#installation)
3. [Set Up SSL Certificates (For MacOS/Linux)](#set-up-ssl-certificates-for-macoslinux)
4. [Run the Application](#run-the-application)

## Prerequisites

### Install Python
Make sure you have Python 3.12 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

### Install PIP
Ensure that you have `pip` installed on your system. Follow the [pip installation guide](https://pip.pypa.io/en/stable/installation/) if it's not already installed.

## Installation
To install the `chatbot-lite` package directly from the GitHub repository, use the following command:

```bash
pip install git+https://github.com/Mahes2/chatbot-lite.git
```

## Set Up SSL Certificates (For MacOS/Linux)

If you encounter SSL certificate issues while making requests, you may need to set up your environment to use proper certificates. You can do this by running the following commands:

```bash
CERT_PATH=$(python -m certifi)
export SSL_CERT_FILE=${CERT_PATH}
export REQUESTS_CA_BUNDLE=${CERT_PATH}
```

## Run the Application

To execute the chatbot, simply run the `main.py` file:

```bash
python main.py
```
