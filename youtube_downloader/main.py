import subprocess

from starlette.responses import RedirectResponse, JSONResponse

from main import app


def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


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
