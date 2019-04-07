import warnings

from fabric import Connection, task

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

PROJECT_NAME = "mdns"
PROJECT_PATH = "~/www"
REPO_URL = "git@github.com:fiit-dbs-2019/dbs2019-project-assignment-nightgaunt.git"


def get_connection(ctx):
    try:
        with Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs) as conn:
            return conn
    except Exception as e:
        return None


@task
def production(ctx):
    ctx.user = "mdns"
    ctx.host = "mdns.jakubdubec.me"
    ctx.connect_kwargs.key_filename = "/Users/jdubec/.ssh/mdns"


@task
def pwd(ctx):
    ctx = get_connection(ctx)
    ctx.run("pwd")


@task
def setup(ctx):
    ctx = get_connection(ctx)

    # Move to project folder
    ctx.run(f"cd {PROJECT_PATH}")

    # Clone repository


@task
def deploy(ctx):
    ctx = get_connection(ctx)

    # Move to project folder
    ctx.run(f"cd {PROJECT_PATH}")
