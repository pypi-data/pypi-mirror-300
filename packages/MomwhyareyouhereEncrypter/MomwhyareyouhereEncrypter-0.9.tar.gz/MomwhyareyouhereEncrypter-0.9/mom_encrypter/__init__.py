from .encrypter import encrypt, decrypt, run
import os
import subprocess

class MomwhyareyouhereEncrypter:
    @staticmethod
    def encrypt(filename):
        with open(filename, 'r') as f:
            content = f.read()
        encrypted_content = 'MOM ENCRYPTED ' * 10 + ''.join([chr(ord(c) + 1) for c in content])
        new_filename = filename.replace(".py", ".mom")
        with open(new_filename, 'w') as f:
            f.write(encrypted_content)
        print(f"Encrypted content written to {new_filename}")

    @staticmethod
    def decrypt(filename):
        with open(filename, 'r') as f:
            content = f.read()
        if 'MOM ENCRYPTED ' * 10 in content:
            content_without_prefix = content.replace('MOM ENCRYPTED ' * 10, '')
            decrypted_content = ''.join([chr(ord(c) - 1) for c in content_without_prefix])
            base_name = filename.replace(".mom", "")
            new_filename = f"{base_name}.py"
            counter = 1
            while os.path.exists(new_filename):
                new_filename = f"{base_name}{counter}.py"
                counter += 1
            with open(new_filename, 'w') as f:
                f.write(decrypted_content)
            print(f"Decrypted content written to {new_filename}")
        else:
            print("The file does not appear to be encrypted.")

    @staticmethod
    def run(filename):
        if not os.path.exists(filename):
            print(f"Error: The file {filename} does not exist.")
            return
        base_name = filename.replace(".mom", "")
        temp_decrypted_file = f"{base_name}_temp.py"

        with open(filename, 'r') as f:
            content = f.read()

        if 'MOM ENCRYPTED ' * 10 in content:
            content_without_prefix = content.replace('MOM ENCRYPTED ' * 10, '')
            decrypted_content = ''.join([chr(ord(c) - 1) for c in content_without_prefix])
            with open(temp_decrypted_file, 'w') as f:
                f.write(decrypted_content)
        else:
            print("The file does not appear to be encrypted.")
            return

        try:
            result = subprocess.run(['python', temp_decrypted_file], capture_output=True, text=True)
            print("Output:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
        finally:
            if os.path.exists(temp_decrypted_file):
                os.remove(temp_decrypted_file)
