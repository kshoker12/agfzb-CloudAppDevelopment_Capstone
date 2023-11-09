from django.db import models
from django.utils.timezone import now
from django.conf import settings
import uuid


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(null = False, max_length=30)
    description = models.CharField(null = False, max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + " Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_TYPES = [
        (SEDAN, "sedan"),
        (SUV, 'suv'),
        (WAGON, 'wagon')
    ]
    carMake = models.ForeignKey(CarMake, on_delete = models.CASCADE)
    name = models.CharField(null = False, max_length=30)
    dealer_id = models.IntegerField()
    model_type = models.CharField(choices=CAR_TYPES, default=SEDAN, max_length=30)
    year = models.DateField(null=True)

    def __str__(self):
        return "Model: " + self.model_type



# # <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name
    


# # <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, id, name, purchase, review, car_make=None, car_model=None, car_year=None, purchase_date=None, sentiment="neutral"):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id  
        self.name = name  
        self.purchase = purchase  
        self.purchase_date = purchase_date
        self.review = review  
        self.sentiment = sentiment  

    def __str__(self):
        return "Review: " + self.review
