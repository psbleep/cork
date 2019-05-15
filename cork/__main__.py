import sys
import click
import cork


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source")
@click.option("-c", "--cleanup", is_flag=True)
@click.option("-f", "--force", is_flag=True)
@click.option("-b", "--browser", default="browsh")
@click.option("-a", "--app", default="app")
@click.option("-p", "--port", "starting_port", type=int, default=5000)
@click.option("--teardown-route", default="teardown")
@click.option("--teardown-function", default="teardown")
def bundle(source, cleanup, force, browser, **kwargs):
    source = source.strip("/")
    platform = cork.get_platform(sys.platform)
    cork.create_corkfile(
        source=source,
        force=force,
        browser=browser,
        **kwargs
    )
    cork.create_executable(source)
    cork.bundle_dependencies(source, browser=browser, platform=platform)
    if cleanup:
        cleanup_list = cork.get_cleanup_list(target=source, dist=False)
        cork.cleanup_files(cleanup_list)


@cli.command()
@click.option("-t", "--target")
@click.option("-f", "--force", is_flag=True)
@click.option("-d", "--dist", is_flag=True)
def cleanup(target, force, dist):
    cleanup_list = cork.get_cleanup_list(target=target, dist=dist)
    cleanup_list_output = ", ".join(cleanup_list)
    if not force:
        click.confirm(
            "Confirm: remove cleanup files {}".format(cleanup_list_output),
            abort=True
        )
    cork.cleanup_files(cleanup_list)
