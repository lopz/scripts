#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import ssl
import datetime
import subprocess 
import sys

import http.client



actions = ["config/export", "config/backup"]

payload = """
{
  "jsonrpc": "2.0",
  "method": "%s",
  "params": {
    "authToken": "c85c70e24e16876238110459b0b11aae83769d8cd69fa1b7a375b6e8cd70ec4c"
   },
  "id": 1
}
"""



filename_backup = "syspass-backup.tar.gz"
filename_crypt = "syspass-backup_%s.zip"

now = datetime.datetime.now()
dt = now.strftime("%Y-%m-%d-%H%M")
filename_crypt = filename_crypt % dt

cmd_docker = "docker run --rm --volumes-from syspass-app --volume $PWD:/backup alpine sh -c 'cd /var/www/html && exec tar -czf /backup/syspass-app-backup.tar.gz sysPass'"
cmd_zip = "zip -p pass123 %s %s" % (filename_crypt, filename_backup)


url_syspass_api = "https://172.20.10.123:49153/api.php"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


conn = http.client.HTTPSConnection(host="172.20.10.123", port=49153, context=ctx)

for action in actions:
  body = payload % action
  conn.request("POST", "/api.php", body=body)
  resp = conn.getresponse()

  if resp.status == 200:
    resp = str(resp.read())
    if "finished" in resp:
      print(resp)
      completed = subprocess.run(cmd_docker, shell=True, stdout=subprocess.PIPE)
      if completed.returncode == 0:
        print(completed.stdout)

completed = subprocess.run(cmd_zip, shell=True, stdout=subprocess.PIPE)
if completed.returncode == 0:
  print(completed.stdout)

conn.close()

