import asyncio

import click
import qrcode
import rich
from rich.console import Console
from rich.table import Table

from decentnet.interface.alias_resolver import AliasResolver
from decentnet.modules.cryptography.asymetric import AsymCrypt
from decentnet.modules.key_util.key_manager import KeyManager


@click.group()
def key():
    pass


@key.command()
@click.option('--private-key-file', '-p', default=None,
              help='Filename for the private key')
@click.option('--public-key-file', '-u', default=None,
              help='Filename for the public key')
@click.option("--description", "-d", default="", help="Description of the key")
@click.option("--sign", "-s", default=False, type=bool, help="Signing keys or Encryption",
              is_flag=True)
@click.option("--alias", "-a", default=None, help="Alias of the key", type=str)
def generate(private_key_file, public_key_file, description, sign, alias):
    """
    Generate SSH key pair.
    """
    asyncio.run(generate_impl(description, private_key_file, public_key_file, sign, alias))


async def generate_impl(description: str, private_key_file: str = None, public_key_file: str = None,
                        sign: bool = False, alias: str = None):
    if sign:
        private_key, o_public_key = KeyManager.generate_singing_key_pair()
        public_key = AsymCrypt.verifying_key_to_string(o_public_key)
    else:
        private_key, o_public_key = KeyManager.generate_encryption_key_pair()
        public_key = KeyManager.key_to_base64(o_public_key)

    private_key = KeyManager.key_to_base64(private_key)

    if private_key_file:
        with open(private_key_file, 'w') as f:
            f.write(private_key)
    if public_key_file:
        with open(public_key_file, 'w') as f:
            f.write(public_key)
    await KeyManager.save_to_db(private_key, public_key, description, not sign, alias)
    rich.print("[green]Generated new key and saved to database[/green]")


@key.command()
def list():
    keys = asyncio.run(KeyManager.get_all_keys())

    table = Table(title="Owned Keys")

    # Define columns
    table.add_column("Alias", justify="left", style="cyan", no_wrap=True)
    table.add_column("Public Key", justify="left", style="magenta")
    table.add_column("Description", justify="left", style="green")
    table.add_column("Can Encrypt", justify="center", style="bold yellow")

    # Add rows to the table
    for key in keys:
        table.add_row(
            key.alias,
            key.public_key,
            key.description,
            "Yes" if key.can_encrypt else "No"
        )

    # Display the table
    console = Console()
    console.print(table)


@key.command()
@click.option("--alias-sign", "-s", required=True, help="Alias of the key for signing")
@click.option("--alias-enc", "-e", required=True, help="Alias of the key for encryption")
@click.option('--qr', is_flag=True, help='Generate a QR code for the keys')
def share(alias_sign: str, alias_enc: str, qr: bool):
    akey, _ = AliasResolver.get_key_by_alias(alias_sign)
    aenc, _ = AliasResolver.get_key_by_alias(alias_enc)
    if qr:
        keys_qr = qrcode.make(akey + aenc)
        keys_qr.show()
    else:
        print(f"{akey}.{aenc}")


@key.command("import")
@click.argument('private_key_path', type=click.Path(exists=True))
@click.argument('public_key_path', type=click.Path(exists=True))
def do_import(private_key_path, public_key_path):
    """
    Import SSH key pair from files.
    """
    private_key_obj, public_key_obj = KeyManager.import_ssh_key_pair(private_key_path,
                                                                     public_key_path)
    private_key, public_key = KeyManager.export_ssh_key_pair(private_key_obj,
                                                             public_key_obj)
    click.echo(f'Private Key:\n{private_key}\n')
    click.echo(f'Public Key:\n{public_key}\n')
