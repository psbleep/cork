import click

import cork


@click.command()
@click.argument("app_source")
def run_cork(app_source):
    app_source = app_source.strip("/")
    cork.create_deploy_script(app_source)
    cork.create_executable(app_source)
