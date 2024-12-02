import secrets

# Generate a random 256-bit secret key (32 bytes)
jwt_secret_key = secrets.token_hex(32)
print(jwt_secret_key)