import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def bs12(file_content, private_key):
    hashed_content = hashlib.sha256(file_content.encode('utf-8')).hexdigest().upper()
    private_key = serialization.load_pem_private_key(
        private_key,
        password=None
    )
    signature = private_key.sign(
        hashed_content.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature
