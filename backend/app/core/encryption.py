import base64

from cryptography.fernet import Fernet

from app.core.config import settings

# This is a simple key derivation. In a real production system, you should use
# a proper key derivation function (KDF) like PBKDF2 or Argon2, and ideally
# a unique key per user. For this example, we'll derive a key from the app's
# secret key.
# Fernet keys must be 32 bytes and URL-safe base64 encoded.
# We'll take the first 32 bytes of the secret key and encode them.
key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
fernet = Fernet(key)


def encrypt(data: str) -> str:
    """Encrypts a string."""
    return fernet.encrypt(data.encode()).decode()


def decrypt(encrypted_data: str) -> str:
    """Decrypts a string."""
    return fernet.decrypt(encrypted_data.encode()).decode()
