from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone



class Coupon(models.Model):
    code = models.CharField(max_length=8, unique=True)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                            MaxValueValidator(100)])

    def __str__(self):
        return self.code


class Sale(models.Model):
    name = models.CharField(max_length=25, unique=True)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                            MaxValueValidator(100)])

    def __str__(self):
        return self.name