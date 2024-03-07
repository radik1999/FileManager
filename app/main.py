from fastapi import FastAPI, Body, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from typing import Annotated

import app.logger_config  # noqa

from app.constants import SESSION_SECRET_KEY, CORS_ORIGINS
from app.deps import GoogleDriveServiceDep, FileToUploadDep
from app.drive import get_files, upload_file, delete_file


app = FastAPI()  # noqa: F811

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        name="home.html",
        context={"request": request}
    )


@app.get("/files")
async def files(request: Request, google_drive_service: GoogleDriveServiceDep, folder_id: str | None = None):
    user_files = get_files(google_drive_service, folder_id)

    context = {"request": request, "files": user_files}

    if folder_id:
        context["folder_id"] = folder_id

    return templates.TemplateResponse(
        name="files.html",
        context=context
    )


@app.post('/upload')
async def upload(
        google_drive_service: GoogleDriveServiceDep,
        file: FileToUploadDep,
        folder_id: Annotated[str | None, Form()] = None
):
    upload_file(google_drive_service, file.filename, file.content_type, folder_id)

    redirect_url = f'/files?folder_id={folder_id}' if folder_id else '/files'
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete('/delete')
async def delete(google_drive_service: GoogleDriveServiceDep, file_id: Annotated[str, Body()]):
    delete_file(google_drive_service, file_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/logout')
async def logout(request: Request):
    request.session.pop('creds')
    request.session.clear()
    return RedirectResponse('/')
