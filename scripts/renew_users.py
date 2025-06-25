from relative_imports import *
from django_setup_script import *
from tqdm import tqdm
from create_users import create_user
from player.models import User


def renew_users() -> None:
    for user in tqdm(User.objects.all(), desc='Deleting users'):
        user.delete()
    
    create_user()


if __name__ == '__main__':
    renew_users()
        