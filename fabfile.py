import os

import fabric

CONNECTION_PROPERTIES = {
    "host": os.environ.get('SERVER_IP'),
    "user": os.environ.get('SERVER_USER'),
    "connect_kwargs": {
        "key_filename": "/home/runner/.ssh/id_rsa-perdana"
    },
}


@fabric.task
def remote(ctx):
    with fabric.Connection(**CONNECTION_PROPERTIES) as c:
        c.local("rm -rf /src/perdana-indonesia-app/env")
        c.run("pwd")
        c.run("sh /src/scripts/deploy.sh")
