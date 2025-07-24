from relative_imports import *
from django_setup_script import *
from pros.models import Social
from utils.constants import POPULAR_SOCIALS


for social in POPULAR_SOCIALS:
    Social.objects.get_or_create(**POPULAR_SOCIALS[social])
