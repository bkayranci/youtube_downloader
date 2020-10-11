import subprocess

from starlette.responses import RedirectResponse, JSONResponse

from main import app




@app.get("/")
async def root(url: str = 'https://www.youtube.com/watch?v=wz0_qJIbkco', download: bool = True):
    if not is_valid_url(url):
        return JSONResponse({
            'detail': 'Not Valid Url'
        },
            status_code=422)

    cmd = subprocess.run(['youtube-dl', '-f', 'best', '--get-url', url], stdout=subprocess.PIPE)
    result = str(cmd.stdout).lstrip("b'").rstrip("\\n'")
    if download:
        return RedirectResponse(result, status_code=302)
    return {'url': result}
