import click
import os
import yaml

from commands.utils.xcproj import list_swift_files


@click.command()
@click.argument('xcodeproj_path')
@click.argument('target_name')
@click.argument('swiftlint_cfg_path')
@click.option('--delete-config/--no-delete-config', default=True)
def lint(xcodeproj_path, target_name, swiftlint_cfg_path, delete_config):
    with open(swiftlint_cfg_path, 'r') as sources:
        sources_config = yaml.load(sources)

        with open('.swiftlint.yml', 'w') as output:
            sources_config['included'] = list_swift_files(xcodeproj_path, target_name)
            yaml.dump(sources_config, output, default_flow_style=False, allow_unicode=True)

        if delete_config:
            try:
                os.remove('.swiftlint.yml')
            except OSError:
                click.echo('Cleanup failed, could not remove .swiftlint.yml file', err=True)

    click.echo('Hello World!')
