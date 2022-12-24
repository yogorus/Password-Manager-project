from cryptography.fernet import Fernet

# Use this to generate for your db
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Use this to load the key
def load_key():
    return open("secret.key", "rb").read()



