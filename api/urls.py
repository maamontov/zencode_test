from django.urls import include, path
from rest_framework_nested import routers

from api.views import ImageViewSet, CommentViewSet, LikeViewSet


router = routers.SimpleRouter()
router.register(r'images', ImageViewSet)

images_router = routers.NestedSimpleRouter(router, r'images', lookup='image')
images_router.register(r'comments', CommentViewSet, basename='image-comments')
images_router.register(r'likes', LikeViewSet, basename='image-likes')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include(images_router.urls)),
]
