from rest_framework import serializers
from ProductsApp.models import Products

#helps convert database data to much simpler to use (in python) format
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('ProductID', 'ProductName', 'ProductDescription', 'Price', 'PhotoFileName')

