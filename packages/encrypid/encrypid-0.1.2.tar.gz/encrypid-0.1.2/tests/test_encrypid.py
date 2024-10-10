# tests/test_encrypid.py

import unittest
from encrypid.encrypid import EncrypId

class TestEncrypId(unittest.TestCase):
    def setUp(self):
        self.password = "senha_segura"
        self.vault = EncrypId(self.password)
        self.credentials = {
            "google": {
                "firebase": {
                    "path_to_credentials": "path/to/firebase.json"
                }
            },
            "gpt": {
                "api_key": "sua_api_key"
            }
        }

    def test_encrypt_decrypt(self):
        data_bytes = b"test data"
        encrypted = self.vault.encrypt_data(data_bytes)
        decrypted = self.vault.decrypt_data(encrypted)
        self.assertEqual(data_bytes, decrypted)

    def test_save_load_credentials(self):
        self.vault.save_encrypted_credentials(self.credentials, "test_encrypted.bin")
        loaded_credentials = self.vault.load_encrypted_credentials("test_encrypted.bin")
        self.assertEqual(self.credentials, loaded_credentials)

    def tearDown(self):
        import os
        if os.path.exists("test_encrypted.bin"):
            os.remove("test_encrypted.bin")

if __name__ == '__main__':
    unittest.main()
