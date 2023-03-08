from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import *

router = DefaultRouter()
router.register('viewset_get_post', ProductViewSet, basename='products')
router.register('modelviewset_crud', ProductModelViewSet)
router.register('product_mixin', ProductMixin)
router.register('category', CategoryAPIView)

urlpatterns = [
    path('func_get/', get_product),
    path('func_post/', post_product),

    path('generic_get/', ProductListGenericView.as_view()),
    path('generic_post/', ProductCreateGenericView.as_view()),
    path('generic_get_post/', ProductListCreateGenericView.as_view()),

    path('apiview_get_post/', ProductAPIView.as_view()),

    path('hello/', get_hello),

    path('', include(router.urls)),

    # path('viewset_get_post/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}))
]