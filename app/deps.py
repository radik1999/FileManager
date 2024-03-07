import os
from typing import Annotated, Any

from fastapi import Depends, UploadFile
from starlette.requests import Request
from google.oauth2.credentials import Credentials
from app.creds_handler import get_user_google_credentials
from app.drive import get_google_drive_service


def user_google_credentials(request: Request):
    return get_user_google_credentials(request.session)


def google_drive_service(creds: Annotated[Credentials, Depends(user_google_credentials)]):
    return get_google_drive_service(creds)


def file_to_upload(file: UploadFile):
    with open(file.filename, "wb") as f:
        f.write(file.file.read())

    yield file

    os.remove(file.filename)


GoogleDriveServiceDep = Annotated[Any, Depends(google_drive_service)]
FileToUploadDep = Annotated[str, Depends(file_to_upload)]
