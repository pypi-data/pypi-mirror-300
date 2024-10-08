import random
import string

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def encrypt(file_name):
    try:
        with open(file_name, 'r') as f:
            content = f.read()
        
        mom_file_name = file_name.replace('.py', '.mom')
        with open(mom_file_name, 'w') as f:
            f.write("MOM ENCRYPTED\n")
            f.write("MOM ENCRYPTED\n")
            f.write(generate_random_string() + "\n")
            f.write(content)
        
        print(f"{file_name} has been encrypted to {mom_file_name}.")
    except Exception as e:
        print(f"Error encrypting file: {e}")

def decrypt(mom_file_name):
    try:
        original_file_name = mom_file_name.replace('.mom', '.py')
        with open(mom_file_name, 'r') as f:
            lines = f.readlines()
        with open(original_file_name, 'w') as f:
            f.writelines(lines[2:])
        
        print(f"{mom_file_name} has been decrypted to {original_file_name}.")
    except Exception as e:
        print(f"Error decrypting file: {e}")

def run(file_name):
    try:
        with open(file_name, 'r') as f:
            exec(f.read())
    except Exception as e:
        print(f"Error running file: {e}")
