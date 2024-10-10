# encrypid_cli.py

import click
from getpass import getpass
import os

import yaml

from encrypid import EncrypId
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env, se existir
load_dotenv()


@click.group()
def cli():
    """EncrypId CLI: Encriptação e Decriptação de Credenciais"""
    pass


@cli.command()
@click.option(
    '--input-file', '-i',
    type=click.Path(exists=True),
    required=True,
    help='Caminho para o arquivo de credenciais YAML a ser encriptado.'
)
@click.option(
    '--output-file', '-o',
    type=click.Path(),
    required=True,
    help='Caminho para salvar o arquivo encriptado.'
)
@click.option(
    '--password', '-p',
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help='Senha para encriptar as credenciais.'
)
def encrypt(input_file, output_file, password):
    """
    Encripta um arquivo de credenciais YAML e salva como um arquivo binário encriptado.
    """
    # Carrega as credenciais do arquivo YAML
    with open(input_file, 'r') as f:
        credentials = yaml.safe_load(f)

    # Instancia o EncrypId
    vault = EncrypId(password)

    # Encripta e salva as credenciais
    vault.save_encrypted_credentials(credentials, output_file)


@cli.command()
@click.option(
    '--input-file', '-i',
    type=click.Path(exists=True),
    required=True,
    help='Caminho para o arquivo encriptado a ser decriptado.'
)
@click.option(
    '--output-file', '-o',
    type=click.Path(),
    help='Caminho para salvar o arquivo YAML decredenciado. Se não for fornecido, as credenciais serão impressas na tela.'
)
@click.option(
    '--password', '-p',
    prompt=True,
    hide_input=True,
    help='Senha para decriptar as credenciais.'
)
def decrypt(input_file, output_file, password):
    """
    Decripta um arquivo binário encriptado e salva como um arquivo YAML ou imprime na tela.
    """
    # Instancia o EncrypId
    vault = EncrypId(password)

    try:
        # Carrega as credenciais decriptadas
        credentials = vault.load_encrypted_credentials(input_file)
    except Exception as e:
        click.echo(f"Falha ao decriptar as credenciais: {e}")
        return

    if output_file:
        # Salva as credenciais em um arquivo YAML
        with open(output_file, 'w') as f:
            yaml.safe_dump(credentials, f)
        click.echo(f"Credenciais decriptadas e salvas em: {output_file}")
    else:
        # Imprime as credenciais na tela
        click.echo("Credenciais decriptadas:")
        click.echo(yaml.safe_dump(credentials, sort_keys=False))


@cli.command()
@click.option(
    '--password', '-p',
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help='Senha para verificar a criptografia.'
)
def generate_key(password):
    """
    Gera uma chave de encriptação baseada na senha fornecida (para demonstração).
    """
    vault = EncrypId(password)
    # Geração de chave não é estritamente necessária aqui, pois a chave é derivada internamente
    click.echo("Chave derivada com sucesso a partir da senha fornecida.")


if __name__ == '__main__':
    cli()
