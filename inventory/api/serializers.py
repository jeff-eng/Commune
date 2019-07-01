from rest_framework import serializers
from inventory.models import Asset, Borrower, Category

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ('first_name',
                  'last_name',
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    borrower = BorrowerSerializer(read_only=True)
    category = serializers.StringRelatedField(many=True)
    condition = serializers.CharField(source='get_condition_display')
    
    class Meta:
        model = Asset
        fields = ('name', 
                  'manufacturer', 
                  'model',
                  'description',
                  'condition',
                  'category',
                  'borrower',
                  'checked_out',
                  'return_date',
                  'is_dueback',
        )