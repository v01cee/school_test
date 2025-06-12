import os
from dotenv import load_dotenv

load_dotenv()


def get_admins():
    admins_str = os.getenv('ADMINS', '')

    if ',' in admins_str:
        admin = [int(id.strip()) for id in admins_str.split(',') if id.strip().isdigit()]
    else:
        admin = [int(id) for id in admins_str.split() if id.isdigit()]

    return admin


