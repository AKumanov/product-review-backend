from rest_flex_fields import is_expanded
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ProductSerializer, ImageSerializer
from .models import Product, Image


# Create your views here.

class ProductViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permit_list_expands = ['category', 'sites', 'comments', 'sites.company', 'sites.productsize']
    filterset_fields = ('category',)

    def get_queryset(self):
        queryset = Product.objects.all()

        if is_expanded(self.request, 'category'):
            queryset = queryset.prefetch_related('category')

        if is_expanded(self.request, 'comments'):
            queryset = queryset.prefetch_related('comments')

        if is_expanded(self.request, 'sites'):
            queryset = queryset.prefetch_related('sites')

        if is_expanded(self.request, 'company'):
            queryset = queryset.prefetch_related('sites__company')

        if is_expanded(self.request, 'productsize'):
            queryset = queryset.prefetch_related('sites__productsize')

        return queryset

    @action(detail=False)
    def get_list(self, request):
        pass

    @action(detail=True)
    def get_product(self, request, pk=None):
        pass

    @action(detail=True, methods=['post', 'delete'])
    def delete_product(self, request, pk=None):
        pass


class ImageViewSet(FlexFieldsModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]
