from rest_framework import serializers
from .models import Drink

#python object to json
class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['id', 'name', 'description', 'cost', 'image']
        # fields = '__all__'
