from relative_imports import *
from django_setup_script import *
from brands.sponsors import business_sponsors
from brands.models import BrandType, Brand


def add_business_sponsors() -> None:
    for sponsor in business_sponsors:
        brand_type = BrandType.objects.get_or_create(name='Business')[0]
        Brand.objects.get_or_create(brand_type=brand_type, **sponsor)


if __name__ == '__main__':
    add_business_sponsors()
