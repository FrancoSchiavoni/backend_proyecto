import bcrypt

def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña usando bcrypt.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    # Generamos el hash.
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # Devolvemos el hash como una cadena de texto para guardarlo en la DB.
    return hashed_password.decode('utf-8')