from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from inventory.api.serializers import AssetSerializer, BorrowerSerializer, CategorySerializer
from inventory.models import Asset, Borrower, Category
from inventory.permissions import IsOwnerOrReadOnly

class AssetRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'uid'
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        # return Asset.objects.filter(owner=self.request.user)
        return Asset.objects.all()

class BorrowerRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Borrower.objects.all()

class AssetList(ListAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view returns a list of all the assets owned by the currently authenticated user.
        """
        return Asset.objects.filter(owner=self.request.user)

class CategoryList(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()

class BorrowerList(ListAPIView):
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Borrower.objects.filter(associated_user=self.request.user)

class AssetCreate(CreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            if name is not None and len(name) < 1:
                raise ValidationError({'name': 'Must be at least one character in length.'})
        except ValueError:
            raise ValidationError({'name': 'Valid characters only.'})
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Asset.objects.filter(owner=self.request.user)

class BorrowerCreate(CreateAPIView):
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Borrower.objects.filter(associated_user=self.request.user)

class CategoryCreate(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()