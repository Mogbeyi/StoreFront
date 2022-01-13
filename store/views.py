from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer
from .models import Collection, Product, OrderItem, Review
from rest_framework import status
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')

        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)

        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        #OrderItem is used directly to filter becasue the product is already fetched in the base class
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an orderitem"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer


    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])

        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it includes one or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    #Get product id from url parameter and return it to review serializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
