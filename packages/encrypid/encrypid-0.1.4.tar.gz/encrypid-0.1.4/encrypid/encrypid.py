# encrypid.py

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import yaml
import re
import sys

# Importações para PyQt5
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt

# Importação para maskpass
import maskpass


class EncrypId:
    def __init__(self, password: str = "", UI: bool = False):
        """
        Inicializa o EncrypId com a senha fornecida. Se a senha estiver vazia,
        solicita ao usuário que a insira via UI ou CLI, dependendo do parâmetro `UI`.

        Parâmetros:
        - password (str): Senha para encriptar e decriptar os dados.
        - UI (bool): Se True, utiliza uma interface gráfica para solicitar a senha.
                     Se False, utiliza a linha de comando.
        """
        if not password:
            password = self.get_password(UI)
        self.password = password

    def derive_key(self, salt: bytes) -> bytes:
        """
        Deriva uma chave criptográfica a partir de uma senha e um salt usando PBKDF2 HMAC SHA256.

        Parâmetros:
        - salt (bytes): Um salt aleatório.

        Retorna:
        - key (bytes): A chave derivada.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Fernet requer chaves de 32 bytes
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
        return key

    def encrypt_data(self, data: bytes) -> bytes:
        """
        Encripta dados usando a senha fornecida.

        Parâmetros:
        - data (bytes): Dados a serem encriptados.

        Retorna:
        - encrypted (bytes): Dados encriptados (salt + encrypted).
        """
        salt = os.urandom(16)  # Gera um salt aleatório
        key = self.derive_key(salt)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        # Armazena o salt + encrypted data
        return salt + encrypted

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Decripta dados encriptados usando a senha fornecida.

        Parâmetros:
        - encrypted_data (bytes): Dados encriptados (salt + encrypted).

        Retorna:
        - decrypted (bytes): Dados decriptados.
        """
        salt = encrypted_data[:16]  # Extrai os primeiros 16 bytes como salt
        encrypted = encrypted_data[16:]
        key = self.derive_key(salt)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted)
        return decrypted

    def save_encrypted_credentials(self, credentials: dict, output_file: str):
        """
        Encripta as credenciais e salva em um arquivo.

        Parâmetros:
        - credentials (dict): Dicionário com as credenciais a serem encriptadas.
        - output_file (str): Caminho para o arquivo de saída encriptado.
        """
        # Converte o dicionário para bytes YAML
        data_bytes = yaml.dump(credentials).encode('utf-8')
        encrypted = self.encrypt_data(data_bytes)
        with open(output_file, 'wb') as f:
            f.write(encrypted)
        print(f"Credenciais encriptadas e salvas em: {output_file}")

    def load_encrypted_credentials(self, input_file: str, returnYaml: bool = True) -> dict:
        """
        Carrega e decripta as credenciais de um arquivo encriptado.

        Parâmetros:
        - input_file (str): Caminho para o arquivo de entrada encriptado.
        - returnYaml (bool): Se True, retorna o YAML desserializado. Caso contrário, retorna os dados brutos.

        Retorna:
        - credentials (dict): Dicionário com as credenciais decriptadas.
        """
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.decrypt_data(encrypted_data)
        if returnYaml:
            return yaml.safe_load(decrypted_data.decode('utf-8'))
        else:
            return decrypted_data

    def encrypt_structure(self, data: dict) -> str:
        """
        Encripta uma estrutura de dados Python e retorna uma string criptografada em Base64.

        Parâmetros:
        - data (dict): Estrutura de dados Python a ser encriptada.

        Retorna:
        - encrypted_base64 (str): Dados encriptados e codificados em Base64.
        """
        # Serializa a estrutura de dados para YAML e codifica em bytes
        data_bytes = yaml.dump(data).encode('utf-8')
        # Encripta os dados
        encrypted_bytes = self.encrypt_data(data_bytes)
        # Codifica os dados encriptados em Base64 para facilitar o armazenamento/transmissão
        encrypted_base64 = base64.urlsafe_b64encode(encrypted_bytes).decode('ascii')
        return encrypted_base64

    def decrypt_structure(self, encrypted_base64: str) -> dict:
        """
        Decripta uma string criptografada em Base64 e retorna a estrutura de dados Python original.

        Parâmetros:
        - encrypted_base64 (str): Dados encriptados e codificados em Base64.

        Retorna:
        - data (dict): Estrutura de dados Python decriptada.
        """
        # Verifica se a string é válida em Base64
        base64_pattern = re.compile(r'^[A-Za-z0-9+/=_-]+$')
        if not base64_pattern.match(encrypted_base64):
            raise ValueError("A string fornecida não é válida em Base64.")

        try:
            # Decodifica a string Base64 para bytes
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_base64)
        except (base64.binascii.Error, ValueError) as e:
            raise ValueError("Falha ao decodificar Base64.") from e

        # Decripta os dados
        decrypted_bytes = self.decrypt_data(encrypted_bytes)
        # Desserializa os bytes YAML para a estrutura de dados Python
        data = yaml.safe_load(decrypted_bytes.decode('utf-8'))
        return data

    def get_password(self, UI: bool) -> str:
        """
        Solicita ao usuário que insira a senha. Se UI for True, utiliza uma interface gráfica.
        Caso contrário, utiliza a linha de comando com entrada oculta.

        Parâmetros:
        - UI (bool): Se True, utiliza a interface gráfica. Se False, utiliza a linha de comando.

        Retorna:
        - password (str): Senha inserida pelo usuário.
        """
        if UI:
            return self._get_password_gui()
        else:
            return self._get_password_cli()

    def _get_password_cli(self) -> str:
        """
        Solicita a senha via linha de comando, ocultando a entrada usando maskpass.

        Retorna:
        - password (str): Senha inserida pelo usuário.
        """
        while True:
            try:
                password = input("Digite a senha: ")
                if password:
                    return password
                else:
                    print("Senha não pode ser vazia. Tente novamente.")
            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário.")
                sys.exit(1)
            except Exception as e:
                print(f"Ocorreu um erro: {e}. Tente novamente.")

    def _get_password_gui(self) -> str:
        """
        Solicita a senha via interface gráfica usando PyQt5.

        Retorna:
        - password (str): Senha inserida pelo usuário.
        """

        class PasswordWindow(QWidget):
            def __init__(self):
                super().__init__()
                self.password = None
                self.init_ui()

            def init_ui(self):
                self.setWindowTitle("Inserir Senha")
                self.setFixedSize(400, 300)

                layout = QVBoxLayout()

                label = QLabel("Digite a senha:")
                label.setAlignment(Qt.AlignCenter)
                layout.addWidget(label)

                self.password_input = QLineEdit()
                self.password_input.setEchoMode(QLineEdit.Password)
                self.password_input.setPlaceholderText("Senha")
                self.password_input.setFixedWidth(300)
                self.password_input.setAlignment(Qt.AlignCenter)
                layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

                submit_button = QPushButton("OK")
                submit_button.clicked.connect(self.submit_password)
                layout.addWidget(submit_button, alignment=Qt.AlignCenter)

                self.error_label = QLabel("")
                self.error_label.setStyleSheet("color: red;")
                self.error_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(self.error_label)

                self.setLayout(layout)

            def submit_password(self):
                pwd = self.password_input.text()
                if pwd:
                    self.password = pwd
                    self.close()
                else:
                    self.error_label.setText("Senha não pode ser vazia. Tente novamente.")

        app = QApplication(sys.argv)
        window = PasswordWindow()
        window.show()
        app.exec_()

        if window.password:
            return window.password
        else:
            raise ValueError("Senha não foi fornecida.")
