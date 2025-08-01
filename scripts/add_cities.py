from tqdm import tqdm
from data.countries import country_list
from profiles.models import CityAndCountry


def add_city() -> None:
    for country_data in tqdm(country_list, desc='Adding countries', unit=' country', leave=True):
        for city in tqdm(country_data['cities'], desc=f'Adding cities of {country_data['name']}', unit=' city'):
            CityAndCountry.objects.get_or_create(
                city=city['name'],
                country=country_data['name']
            )

if __name__ == '__main__':
    add_city()