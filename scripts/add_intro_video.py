from relative_imports import *
from django_setup_script import *
from profiles.models import IntroVideo, User
from tqdm import tqdm


def add_intro_video() -> None:
    users = list(User.objects.all())

    for user in tqdm(
        users, desc='Adding intro video...', unit=' user', leave=True):
        IntroVideo.objects.get_or_create(user=user, url='https://i.imgur.com/BnDntB8.mp4')


if __name__ == '__main__':
    add_intro_video()
