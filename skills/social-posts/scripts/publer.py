#!/usr/bin/env python3
"""Upload images from this computer to your Publer media library.

The Publer connector (MCP) can attach an image from a web address, or a file
shared in a ChatGPT chat, but not a file on your computer. This script sends
local images up through Publer's API and prints a media id for each, which the
AI then attaches to the post.

    python3 publer.py upload FILE [FILE ...]   prints "<media id>  <file>" for each file
    python3 publer.py workspaces               lists your workspaces

Needs a Publer API key (Business plan): Publer, Settings, Access & Login, API Keys.
Keep the key out of chats. Store it once, in your own terminal:

    Mac:      security add-generic-password -a "$USER" -s publer-api-key -w
    Windows:  setx PUBLER_API_KEY "your key"   (then open a new terminal)
    Linux:    export PUBLER_API_KEY="your key" in your shell profile

The workspace is PUBLER_WORKSPACE_ID, else --workspace NAME, else your only one.
Uses only Python's standard library.
"""
import argparse, json, mimetypes, os, platform, subprocess, sys, urllib.error, urllib.request, uuid

API = 'https://app.publer.com/api/v1'


def key():
    k = os.environ.get('PUBLER_API_KEY', '').strip()
    if not k and platform.system() == 'Darwin':
        r = subprocess.run(['security', 'find-generic-password', '-a', os.environ.get('USER', ''),
                            '-s', 'publer-api-key', '-w'], capture_output=True, text=True)
        k = r.stdout.strip()
    if not k:
        sys.exit('No Publer API key found. See the top of this file for how to store one.')
    return k


def call(path, workspace=None, body=None, content_type=None):
    req = urllib.request.Request(f'{API}/{path}', data=body, method='POST' if body else 'GET')
    req.add_header('Authorization', f'Bearer-API {key()}')
    # Publer sits behind Cloudflare, which refuses Python's default user agent.
    req.add_header('User-Agent', 'social-posts-kit/1.0')
    if workspace:
        req.add_header('Publer-Workspace-Id', workspace)
    if content_type:
        req.add_header('Content-Type', content_type)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read() or b'null')
    except urllib.error.HTTPError as e:
        sys.exit(f'Publer said no ({e.code}): {e.read().decode(errors="replace")[:300]}')


def workspaces():
    data = call('workspaces')
    return data if isinstance(data, list) else data.get('workspaces', [])


def workspace_id(name):
    if os.environ.get('PUBLER_WORKSPACE_ID'):
        return os.environ['PUBLER_WORKSPACE_ID']
    ws = workspaces()
    pick = [w for w in ws if not name or w.get('name', '').lower() == name.lower()]
    if len(pick) != 1:
        sys.exit('Choose a workspace with --workspace NAME: ' + ', '.join(w.get('name', '?') for w in ws))
    return pick[0]['id']


def upload(path, workspace):
    boundary = uuid.uuid4().hex
    name = os.path.basename(path)
    kind = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    with open(path, 'rb') as f:
        data = f.read()
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="in_library"\r\n\r\ntrue\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\n'
            f'Content-Type: {kind}\r\n\r\n').encode() + data + f'\r\n--{boundary}--\r\n'.encode()
    return call('media', workspace, body, f'multipart/form-data; boundary={boundary}')['id']


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--workspace', help='workspace name, when you have more than one')
    sub = p.add_subparsers(dest='cmd', required=True)
    up = sub.add_parser('upload'); up.add_argument('files', nargs='+')
    sub.add_parser('workspaces')
    a = p.parse_args()
    if a.cmd == 'workspaces':
        for w in workspaces():
            print(f'{w.get("id")}  {w.get("name")}')
        return
    ws = workspace_id(a.workspace)
    for f in a.files:
        if not os.path.isfile(f):
            sys.exit(f'No file at {f}')
        print(f'{upload(f, ws)}  {f}')


if __name__ == '__main__':
    main()
