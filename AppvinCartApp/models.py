

from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_available = models.BooleanField(default=True)

    # Add any additional fields as needed

