import re
import subprocess

from fastapi import FastAPI
from starlette.responses import RedirectResponse, JSONResponse

app = FastAPI()

from youtube_downloader.main import *
