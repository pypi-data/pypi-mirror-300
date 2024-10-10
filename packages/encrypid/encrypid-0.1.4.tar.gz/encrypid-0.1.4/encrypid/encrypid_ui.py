# encrypid_ui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
    QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QTabWidget
)
from PyQt5.QtCore import Qt
from encrypid import EncrypId
import yaml
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env, se existir
load_dotenv()


class EncrypIdUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EncrypId - Gerenciador de Credenciais')
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        main_layout = QVBoxLayout()

        # Tabs para Encrypt e Decrypt
        self.tabs = QTabWidget()
        self.encrypt_tab = QWidget()
        self.decrypt_tab = QWidget()

        self.tabs.addTab(self.encrypt_tab, "Encriptar Credenciais")
        self.tabs.addTab(self.decrypt_tab, "Decriptar Credenciais")

        # Configurar cada tab
        self.init_encrypt_tab()
        self.init_decrypt_tab()

        # Área de logs
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText("Logs e mensagens aparecerão aqui...")

        # Adicionar widgets ao layout principal
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(QLabel("Logs:"))
        main_layout.addWidget(self.log_text)

        self.setLayout(main_layout)

    def init_encrypt_tab(self):
        layout = QVBoxLayout()

        # Selecionar arquivo YAML de entrada
        input_layout = QHBoxLayout()
        self.encrypt_input_label = QLabel("Arquivo YAML de Entrada:")
        self.encrypt_input_path = QLineEdit()
        self.encrypt_input_browse = QPushButton("Procurar")
        self.encrypt_input_browse.clicked.connect(self.browse_encrypt_input)
        input_layout.addWidget(self.encrypt_input_label)
        input_layout.addWidget(self.encrypt_input_path)
        input_layout.addWidget(self.encrypt_input_browse)
        layout.addLayout(input_layout)

        # Selecionar local para salvar arquivo encriptado
        output_layout = QHBoxLayout()
        self.encrypt_output_label = QLabel("Arquivo Encriptado de Saída:")
        self.encrypt_output_path = QLineEdit()
        self.encrypt_output_browse = QPushButton("Procurar")
        self.encrypt_output_browse.clicked.connect(self.browse_encrypt_output)
        output_layout.addWidget(self.encrypt_output_label)
        output_layout.addWidget(self.encrypt_output_path)
        output_layout.addWidget(self.encrypt_output_browse)
        layout.addLayout(output_layout)

        # Campo de senha
        password_layout = QHBoxLayout()
        self.encrypt_password_label = QLabel("Senha:")
        self.encrypt_password_input = QLineEdit()
        self.encrypt_password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.encrypt_password_label)
        password_layout.addWidget(self.encrypt_password_input)
        layout.addLayout(password_layout)

        # Botão de encriptação
        self.encrypt_button = QPushButton("Encriptar Credenciais")
        self.encrypt_button.clicked.connect(self.encrypt_credentials)
        layout.addWidget(self.encrypt_button)

        self.encrypt_tab.setLayout(layout)

    def init_decrypt_tab(self):
        layout = QVBoxLayout()

        # Selecionar arquivo encriptado de entrada
        input_layout = QHBoxLayout()
        self.decrypt_input_label = QLabel("Arquivo Encriptado de Entrada:")
        self.decrypt_input_path = QLineEdit()
        self.decrypt_input_browse = QPushButton("Procurar")
        self.decrypt_input_browse.clicked.connect(self.browse_decrypt_input)
        input_layout.addWidget(self.decrypt_input_label)
        input_layout.addWidget(self.decrypt_input_path)
        input_layout.addWidget(self.decrypt_input_browse)
        layout.addLayout(input_layout)

        # Selecionar local para salvar arquivo YAML de saída (opcional)
        output_layout = QHBoxLayout()
        self.decrypt_output_label = QLabel("Arquivo YAML de Saída (Opcional):")
        self.decrypt_output_path = QLineEdit()
        self.decrypt_output_browse = QPushButton("Procurar")
        self.decrypt_output_browse.clicked.connect(self.browse_decrypt_output)
        output_layout.addWidget(self.decrypt_output_label)
        output_layout.addWidget(self.decrypt_output_path)
        output_layout.addWidget(self.decrypt_output_browse)
        layout.addLayout(output_layout)

        # Campo de senha
        password_layout = QHBoxLayout()
        self.decrypt_password_label = QLabel("Senha:")
        self.decrypt_password_input = QLineEdit()
        self.decrypt_password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.decrypt_password_label)
        password_layout.addWidget(self.decrypt_password_input)
        layout.addLayout(password_layout)

        # Botão de decriptação
        self.decrypt_button = QPushButton("Decriptar Credenciais")
        self.decrypt_button.clicked.connect(self.decrypt_credentials)
        layout.addWidget(self.decrypt_button)

        self.decrypt_tab.setLayout(layout)

    def browse_encrypt_input(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Selecione o Arquivo YAML de Entrada", "",
            "YAML Files (*.yaml *.yml);;All Files (*)", options=options)
        if file_name:
            self.encrypt_input_path.setText(file_name)

    def browse_encrypt_output(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Selecione o Local para Salvar o Arquivo Encriptado", "",
            "Bin Files (*.bin);;All Files (*)", options=options)
        if file_name:
            self.encrypt_output_path.setText(file_name)

    def browse_decrypt_input(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Selecione o Arquivo Encriptado de Entrada", "",
            "Bin Files (*.bin);;All Files (*)", options=options)
        if file_name:
            self.decrypt_input_path.setText(file_name)

    def browse_decrypt_output(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Selecione o Local para Salvar o Arquivo YAML Decriptado", "",
            "YAML Files (*.yaml *.yml);;All Files (*)", options=options)
        if file_name:
            self.decrypt_output_path.setText(file_name)

    def encrypt_credentials(self):
        input_file = self.encrypt_input_path.text().strip()
        output_file = self.encrypt_output_path.text().strip()
        password = self.encrypt_password_input.text()

        if not input_file or not output_file or not password:
            self.show_message("Erro", "Por favor, preencha todos os campos obrigatórios.", QMessageBox.Warning)
            return

        # Carrega as credenciais do arquivo YAML
        try:
            with open(input_file, 'r') as f:
                credentials = yaml.safe_load(f)
        except Exception as e:
            self.log(f"Erro ao carregar o arquivo YAML: {e}")
            self.show_message("Erro", f"Erro ao carregar o arquivo YAML:\n{e}", QMessageBox.Critical)
            return

        # Instancia o EncrypId
        try:
            vault = EncrypId(password)
            vault.save_encrypted_credentials(credentials, output_file)
            self.log(f"Credenciais encriptadas e salvas em: {output_file}")
            self.show_message("Sucesso", "Credenciais encriptadas com sucesso!", QMessageBox.Information)
        except Exception as e:
            self.log(f"Erro ao encriptar as credenciais: {e}")
            self.show_message("Erro", f"Erro ao encriptar as credenciais:\n{e}", QMessageBox.Critical)

    def decrypt_credentials(self):
        input_file = self.decrypt_input_path.text().strip()
        output_file = self.decrypt_output_path.text().strip()
        password = self.decrypt_password_input.text()

        if not input_file or not password:
            self.show_message("Erro", "Por favor, preencha os campos obrigatórios.", QMessageBox.Warning)
            return

        # Instancia o EncrypId
        try:
            vault = EncrypId(password)
            credentials = vault.load_encrypted_credentials(input_file)
            self.log(f"Credenciais decriptadas com sucesso de: {input_file}")

            if output_file:
                # Salva as credenciais em um arquivo YAML
                with open(output_file, 'w') as f:
                    yaml.safe_dump(credentials, f)
                self.log(f"Credenciais decriptadas e salvas em: {output_file}")
                self.show_message("Sucesso", f"Credenciais decriptadas e salvas em:\n{output_file}", QMessageBox.Information)
            else:
                # Exibe as credenciais na tela
                credentials_str = yaml.safe_dump(credentials, sort_keys=False)
                self.show_message("Credenciais Decriptadas", credentials_str, QMessageBox.Information)
        except Exception as e:
            self.log(f"Erro ao decriptar as credenciais: {e}")
            self.show_message("Erro", f"Erro ao decriptar as credenciais:\n{e}", QMessageBox.Critical)

    def log(self, message):
        self.log_text.append(message)

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()


def main():
    app = QApplication(sys.argv)
    window = EncrypIdUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
