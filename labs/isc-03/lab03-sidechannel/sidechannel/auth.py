# Main authentication routines

# HEY, DON'T CHEAT!
SECRET_PASSWORD = "Flag{5mall0ne}"
LENGTH = len(SECRET_PASSWORD)


def check_password(password: str) -> bool:
    """
    A timing side-channel attack vulnerable password checking routine.
    """
    for i, c in enumerate(SECRET_PASSWORD):
        x = password[i] if i < len(password) else ''
        if c != x:
            return False
    return True


