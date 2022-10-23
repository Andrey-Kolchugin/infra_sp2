from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet)

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
v1_router.register('users', views.AdminUserViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', views.SignUp.as_view()),
    path('v1/auth/token/', views.ObtainToken.as_view()),
]
