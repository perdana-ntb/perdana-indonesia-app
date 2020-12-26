from fabric import Connection, task

CONNECTION_PROPERTIES = {
    "host": "159.65.143.247",
    "user": "root",
    "connect_kwargs": {
        "key_filename": "/src/rsa/perdana_rsa"
    },
}


@task
def remote(ctx):
    with Connection(**CONNECTION_PROPERTIES) as c:
        c.local("rm -rf /src/perdana-indonesia-app/env")
        c.run("pwd")
        c.run("sh /src/scripts/deploy.sh")
