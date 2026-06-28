# generate_admin.py

import bcrypt

hashed = bcrypt.hashpw(
    "admin123".encode(),
    bcrypt.gensalt()
).decode()

print(hashed)