from django.db import models


class BrandType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    brand_type = models.ForeignKey(BrandType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    formal_name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField()

    @classmethod
    def all_details(cls) -> dict[str, list]:
        brand_types = BrandType.objects.all().exclude(name='Business')
        brands: dict[str, list] = dict()
        for brand_type in brand_types:
            for brand in cls.objects.filter(brand_type=brand_type):
                if brand_type.name in brands:
                    brands[brand_type.name].append(dict(
                        brand_id=brand.id,
                        brandType=brand.brand_type.name,
                        name=brand.name,
                        formal_name=brand.formal_name,
                        logo_url=brand.logo_url
                    ))
                else: brands[brand_type.name] = [dict(
                        brand_id=brand.id,
                        brandType=brand.brand_type.name,
                        name=brand.name,
                        formal_name=brand.formal_name,
                        logo_url=brand.logo_url
                    )]
        return brands
    
    @property
    def details(self) -> list[dict]:
        return dict(
            brand_id=self.id,
            brandType=self.brand_type.name,
            name=self.name,
            formal_name=self.formal_name,
            logo_url=self.logo_url
        )

    def __str__(self) -> str:
        return f'{self.formal_name} ({self.brand_type.name})'


