import json
import logging
import os

from fastapi import HTTPException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from starlette import status

from app.constants import GOOGLE_CONSOLE_SCOPES, GOOGLE_CONSOLE_CREDENTIALS_FILE

logger = logging.getLogger(__name__)


def get_user_google_credentials(session):
    if creds := session.get("creds"):
        creds = Credentials.from_authorized_user_info(creds, GOOGLE_CONSOLE_SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        creds = request_user_google_credentials()
        session["creds"] = json.loads(creds.to_json())

    return creds


def request_user_google_credentials():
    if os.path.exists(GOOGLE_CONSOLE_CREDENTIALS_FILE):
        flow = InstalledAppFlow.from_client_secrets_file(
            GOOGLE_CONSOLE_CREDENTIALS_FILE, GOOGLE_CONSOLE_SCOPES
        )
        creds = flow.run_local_server(port=0)

        logger.info("User got credentials from google")
        return creds
    else:
        logger.error(f"Could not find file{GOOGLE_CONSOLE_CREDENTIALS_FILE} with google oauth credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find google oauth credentials",
        )
