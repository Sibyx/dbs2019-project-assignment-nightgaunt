import datetime
import json
import os
import warnings

from fabric import Connection, task
from invoke import Context

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

PROJECT_NAME = "mdns"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_URL = "https://github.com/Sibyx/mdns.git"
KEEP_RELEASES = 5


def _get_connection(ctx: Context, config: dict) -> Connection:
    ctx.host = config['host']
    ctx.user = config['user']
    ctx.connect_kwargs.key_filename = config['private_key']
    ctx.port = config['port']

    ctx = Connection(
        host=ctx.host,
        user=ctx.user,
        port=ctx.port,
        connect_kwargs=ctx.connect_kwargs,
    )

    ctx.config['run']['echo'] = True

    return ctx


def _parse_config(destination: str) -> dict:
    with open(f"{BASE_DIR}/.deploy/{destination}.json") as conf_file:
        return json.load(conf_file)


@task
def check(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])

    ctx.run(f'{config["interpreter"]} --version')


@task
def setup(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])
    shared_env = f"{config['deploy_to']}/shared/env"

    ctx.run(f"mkdir {config['deploy_to']}")

    with ctx.cd(config['deploy_to']):
        # Create directory structure
        ctx.run(f"mkdir shared")
        ctx.run(f"mkdir shared/logs")
        ctx.run(f"mkdir shared/media")
        ctx.run(f"mkdir releases")

        # Create Python virtualenv
        ctx.run(f"{config['interpreter']} -m venv shared/env")

        # Install deployment tools
        ctx.run(f"{shared_env}/bin/pip install pipfile-requirements")


@task
def deploy(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])

    release = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    shared_env = f"{config['deploy_to']}/shared/env"

    # Set deploy to as current directory
    with ctx.cd(f"{config['deploy_to']}/releases"):
        # Clone repository
        ctx.run(f"git clone {REPO_URL} {release}")

    # Set current release directory as working directory
    with ctx.cd(f"{config['deploy_to']}/releases/{release}"):
        # Checkout correct revision
        ctx.run(f"git checkout {config['revision']}")
        # Just to be sure, run git pull
        ctx.run("git pull")

        # Install & update dependencies
        ctx.run(f"{shared_env}/bin/pip install --upgrade pip")
        ctx.run(f"{shared_env}/bin/pip install --upgrade pipfile-requirements")
        ctx.run(f"{shared_env}/bin/pipfile2req Pipfile.lock > requirements.txt")
        ctx.run(f"{shared_env}/bin/pip install -r requirements.txt")

        # Create .env file
        ctx.run("touch .env")
        for key, value in config['env'].items():
            ctx.run(f'echo "{key}=\'{value}\'" >> .env')

        # Create symlinks for logs
        ctx.run(f"ln -s {config['deploy_to']}/shared/logs logs")
        ctx.run("touch logs/error.log")
        ctx.run("touch logs/request.log")
        ctx.run("touch logs/sql.log")

        # Create symlink for media
        ctx.run(f"rm -rf media")
        ctx.run(f"ln -s {config['deploy_to']}/shared/media media")

        # Migrate
        ctx.run(
            f"DJANGO_SETTINGS_MODULE={config['env']['DJANGO_SETTINGS_MODULE']} "
            f"{shared_env}/bin/python manage.py migrate --no-input"
        )

        # Static files
        ctx.put("static/bundle.js", f"{config['deploy_to']}/releases/{release}/static/")
        ctx.put("static/bundle.js.map", f"{config['deploy_to']}/releases/{release}/static/")

        # Removing sensitive data
        ctx.run(f"rm -rf .deploy Pipfile Pipfile.lock requirements.txt")

    # Publish release
    with ctx.cd(config['deploy_to']):
        # Remove old symlink
        ctx.run("rm -f current")
        # Create symlink to the latest release
        ctx.run(f"ln -s {config['deploy_to']}/releases/{release} current")

    # Restart Gunicorn service
    # ctx.run("sudo systemctl restart mdns-web")

    # Clean old releases
    with ctx.cd(f"{config['deploy_to']}/releases"):
        ctx.run(f"ls -t . | sort -r | tail -n +{KEEP_RELEASES + 1} | xargs rm -rf --")


@task
def clean(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])

    ctx.run(f"rm -rf {config['deploy_to']}")


@task
def user(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])
    shared_env = f"{config['deploy_to']}/shared/env"

    # Move to project folder
    with ctx.cd(f"{config['deploy_to']}/current"):
        ctx.run(
            f"DJANGO_SETTINGS_MODULE={config['env']['DJANGO_SETTINGS_MODULE']} "
            f"{shared_env}/bin/python manage.py createsuperuser", pty=True
        )


@task
def fake(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])
    shared_env = f"{config['deploy_to']}/shared/env"

    # Move to project folder
    with ctx.cd(f"{config['deploy_to']}/current"):
        ctx.run(
            f"DJANGO_SETTINGS_MODULE={config['env']['DJANGO_SETTINGS_MODULE']} "
            f"{shared_env}/bin/python manage.py fake --clear", pty=True
        )


@task
def organisms(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])
    shared_env = f"{config['deploy_to']}/shared/env"

    # Move to project folder
    with ctx.cd(f"{config['deploy_to']}/current"):
        ctx.put("tmp/data.csv", f"{config['deploy_to']}/current/tmp")

        ctx.run(
            f"DJANGO_SETTINGS_MODULE={config['env']['DJANGO_SETTINGS_MODULE']} "
            f"{shared_env}/bin/python manage.py import_organisms --file tmp/data.csv", pty=True
        )


@task
def restart(ctx, destination):
    config = _parse_config(destination)
    ctx = _get_connection(ctx, config['ssh'])

    # Restart Gunicorn service
    ctx.run("sudo systemctl restart mdns-web", pty=True)
