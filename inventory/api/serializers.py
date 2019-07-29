from rest_framework import serializers
from inventory.models import Asset, Borrower, Category

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ('first_name',
                  'last_name',
                  'associated_user'
        )
    
    def update(self, instance, validated_data):
        print('Update method triggered.')
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.associated_user = validated_data.get('associated_user'. instance.associated_user)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    borrower = BorrowerSerializer(allow_null=True)
    category = serializers.StringRelatedField(many=True)
    condition = serializers.ChoiceField(choices=Asset.CONDITION_TYPE, default='g')
    
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
        depth = 1

    def update(self, instance, validated_data):
        instance.borrower = validated_data.get('borrower')
        instance.return_date = validated_data.get('return_date')
        instance.checked_out = validated_data.get('checked_out')
        instance.save()
        return instance