import subprocess

from flask import Flask, redirect, request, jsonify, make_response

app = Flask(__name__)


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


@app.route("/")
def home_view():
    url = request.args.get('url')
    download = request.args.get('download')
    if not is_valid_url(url):
        return make_response((jsonify({
            'detail': 'Not Valid Url'
        }), 422))

    cmd = subprocess.run(['youtube-dl', '-f', 'best', '--get-url', url], stdout=subprocess.PIPE)
    result = str(cmd.stdout).lstrip("b'").rstrip("\\n'")
    if download != 'false':
        return redirect(result)
    return {'url': result}
