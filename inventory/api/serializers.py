from django.conf import settings
from rest_framework import serializers
from inventory.models import Asset, Borrower, Category

class BorrowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrower
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'associated_user',
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.associated_user = validated_data.get('associated_user'. instance.associated_user)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name')

class AssetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_null=True)
    description = serializers.CharField(allow_null=True)
    manufacturer = serializers.CharField(allow_null=True)
    uid = serializers.UUIDField(read_only=True, allow_null=True)
    borrower = BorrowerSerializer(allow_null=True, read_only=True)
    condition = serializers.ChoiceField(choices=Asset.CONDITION_TYPE, default='g', allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    return_date = serializers.DateField(allow_null=True)
    checked_out = serializers.BooleanField(allow_null=True)
    category = CategorySerializer(required=False, many=True)

    class Meta:
        model = Asset
        fields = ('uid',
                  'name', 
                  'manufacturer', 
                  'model',
                  'description',
                  'owner',
                  'condition',
                  'category',
                  'borrower',
                  'checked_out',
                  'return_date',
                  'is_dueback',
        )

    def update(self, instance, validated_data):
        instance.borrower = validated_data.get('borrower', instance.borrower)
        instance.return_date = validated_data.get('return_date', instance.return_date)
        instance.checked_out = validated_data.get('checked_out', instance.checked_out)
        
        instance.name = validated_data.get('name', instance.name)
        instance.manufacturer = validated_data.get('manufacturer', instance.manufacturer)
        instance.model = validated_data.get('model', instance.model)
        instance.description = validated_data.get('description', instance.description)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

    def create(self, validated_data):
        return Asset.objects.create(**validated_data)
