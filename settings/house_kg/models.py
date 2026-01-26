from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = (
    ('Buyer', 'Buyer'),
    ('Seller', 'Seller')
)

PROPERTY_CHOICES = (
    ('Apartment', 'Apartment'),
    ('House', 'House'),
    ('Commercial real estate', 'Commercial real estate'),
    ('Room', 'Room'),
    ('Plot', 'Plot'),
    ('Cottage', 'Cottage'),
    ('Garage/parking', 'Garage/parking')
)

REGION_CHOICES = (
    ('BISHKEK', 'Bishkek'),
    ('OSH_CITY', 'Osh'),
    ('CHUI', 'Chui'),
    ('OSH', 'Osh'),
    ('JALAL_ABAD', 'Jalal-Abad'),
    ('BATKEN', 'Batken'),
    ('NARYN', 'Naryn'),
    ('ISSYK_KUL', 'Issyk-Kul'),
    ("TALAS", 'Talas'),
)

CONDITION_CHOICES = (
    ('For finishing', 'For finishing'),
    ('European style renovation', 'European style renovation'),
    ('Good', 'Good'),
    ('Middle', 'Middle'),
    ('Not finished', 'Not finished')
)

class UserProfile(AbstractUser):
    status = models.CharField(choices=STATUS_CHOICES, default='Buyer')
    phone_number = PhoneNumberField(null=True, blank=True)
    registered_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class City(models.Model):
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name

class District(models.Model):
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return self.district_name

class Property(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    property_type = models.CharField(choices=PROPERTY_CHOICES)
    region = models.CharField(choices=REGION_CHOICES)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    area = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=10)
    price = models.PositiveSmallIntegerField()
    rooms = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    total_floors = models.PositiveSmallIntegerField(null=True, blank=True)
    condition = models.CharField(choices=CONDITION_CHOICES)
    images = models.ImageField(upload_to='property_images/', null=True, blank=True)
    documents = models.FileField(upload_to='property_documents/', null=True, blank=True)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.price}'

class Review(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_buyer')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_seller')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.buyer} > {self.seller}: {self.rating}/10'