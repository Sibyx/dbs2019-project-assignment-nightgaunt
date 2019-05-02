import warnings

from fabric import Connection, task

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

PROJECT_NAME = "mdns"
PROJECT_PATH = "~/www"
REPO_URL = "git@github.com:fiit-dbs-2019/dbs2019-project-assignment-nightgaunt.git"
BRANCH = 'master'


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
def setup(ctx):
    ctx = get_connection(ctx)

    # Clone repository
    ctx.run(f"git clone {REPO_URL} {PROJECT_PATH}")


@task
def deploy(ctx):
    ctx = get_connection(ctx)

    # Move to project folder
    with ctx.cd(f"{PROJECT_PATH}"):
        # Download changes
        ctx.run(f"git checkout {BRANCH}")
        ctx.run(f"git pull")

        # Setup env
        ctx.run("pipenv sync --dev", pty=True)

        # Run migrations
        ctx.run("pipenv run python manage.py migrate")

        # Static files
        ctx.put("static/bundle.js", f"www/static")
        ctx.put("static/bundle.js.map", f"www/static")

        # Restart Gunicorn service
        ctx.run("sudo systemctl restart mdns-web")


@task
def user(ctx):
    ctx = get_connection(ctx)

    # Move to project folder
    with ctx.cd(f"{PROJECT_PATH}"):
        ctx.run("pipenv run python manage.py createsuperuser", pty=True)


@task
def fake(ctx):
    ctx = get_connection(ctx)

    # Move to project folder
    with ctx.cd(f"{PROJECT_PATH}"):
        # Execute fake command
        ctx.run("pipenv run python manage.py fake --clear", pty=True)


@task
def organisms(ctx):
    ctx = get_connection(ctx)

    # Move to project folder
    with ctx.cd(f"{PROJECT_PATH}"):
        ctx.put("tmp/data.csv", f"www/tmp")

        # Execute fake command
        ctx.run("pipenv run python manage.py import_organisms --file tmp/data.csv")


@task
def restart(ctx):
    ctx = get_connection(ctx)

    # Restart Gunicorn service
    ctx.run("sudo systemctl restart mdns-web", pty=True)
