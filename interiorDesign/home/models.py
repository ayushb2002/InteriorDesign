from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField

# Create your models here.
class Shop(models.Model):
    desc = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2) 

    def __str__(self):
        return f"{self.id} - {self.desc} | ${self.price}"

    class Meta:
        verbose_name_plural = "Shop"

class Orders(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Shop, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=True)
    status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.email} - {self.item.desc}. Delivered at {self.address}"

    class Meta:
        verbose_name_plural = "Orders"

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return f"{self.user.username} - {self.address}. Contact -  {self.phone}"

    class Meta:
        verbose_name_plural = "Bookings"