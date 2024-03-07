import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger(__name__)


def get_google_drive_service(user_creds):
    return build("drive", "v3", credentials=user_creds)


def get_files(drive_service, folder_id=None):
    params = {
        "pageSize": 30,
        "fields": "nextPageToken, files(id, name, mimeType, iconLink, webViewLink)",
    }

    if folder_id:
        params["q"] = f"parents = '{folder_id}'"

    results = (
        drive_service.files()
        .list(**params)
        .execute()
    )

    items = results.get("files", [])
    return items


def upload_file(drive_service, file_name, mime_type, folder_id=None):
    media = MediaFileUpload(file_name, mimetype=mime_type)

    file_metadata = {"name": file_name}

    if folder_id:
        file_metadata["parents"] = [folder_id]

    drive_service.files().create(media_body=media, body=file_metadata).execute()
    logger.info(f"File {file_name} was uploaded")


def delete_file(drive_service, file_id):
    try:
        drive_service.files().delete(fileId=file_id).execute()
        logger.info(f"File with id {file_id} was deleted")
    except HttpError as e:
        logger.error(f"An error occurred during file deletion:\n {e.error_details}")
