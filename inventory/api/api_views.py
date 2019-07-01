from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from inventory.api.serializers import AssetSerializer, BorrowerSerializer, CategorySerializer
from inventory.models import Asset, Borrower, Category

class AssetRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'uid'
    serializer_class = AssetSerializer

    def get_queryset(self):
        user = self.request.user
        return Asset.objects.filter(owner=user)

class AssetList(ListAPIView):
    serializer_class = AssetSerializer

    def get_queryset(self):
        """
        This view returns a list of all the assets owned by the currently authenticated user.
        """
        user = self.request.user
        return Asset.objects.filter(owner=user)

class AssetCreate(CreateAPIView):
    serializer_class = AssetSerializer

    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            if name is not None and len(name) < 1:
                raise ValidationError({'name': 'Must be at least one character in length.'})
        except ValueError:
            raise ValidationError({'name': 'Valid characters only.'})
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Asset.objects.filter(owner=user)

class BorrowerCreate(CreateAPIView):
    serializer_class = BorrowerSerializer

    def get_queryset(self):
        user = self.request.user
        return Borrower.objects.filter(associated_user=user)

class CategoryCreate(CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryList(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()