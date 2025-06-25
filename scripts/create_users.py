from django.contrib.auth import get_user_model
from utils.stuff import names, gradient_colors
from player.models import LevelXPMapping
User = get_user_model()
from tqdm import tqdm


def create_user() -> None:
    for name in tqdm(names, desc='Creating new users', unit=' user', leave=True):
        first_name, last_name = name.split()
        email = first_name + '@bowlersnetwork_v1.com'
        if not User.objects.filter(
            username=first_name).exists():
            user = User.objects.create(
                username=first_name, 
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password('prottoy21')
            user.save()

def create_levels() -> None:
    LevelXPMapping.objects.all().delete()
    current_max = 9
    for index, color in enumerate(gradient_colors):
        max_xp = current_max + (index * 10)
        current_max = max_xp 
        level = index + 1
        card_theme_color = color
        LevelXPMapping.objects.create(max_xp=max_xp, level=level, card_theme_color=card_theme_color)
         