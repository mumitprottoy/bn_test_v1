from data.countries import country_list
from profiles.models import CityAndCountry

def add_city() -> None:
    for country_data in country_list:
        for city in country_data['cities']:
            CityAndCountry.objects.get_or_create(
                city=city,
                country=country_data['country']
            )

if __name__ == '__main__':
    add_city()