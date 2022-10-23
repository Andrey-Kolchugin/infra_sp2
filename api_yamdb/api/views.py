from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title
from users.permissions import UserPermissions

from .permissions import AuthorModerAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ObtainTokenSerializer,
                          ReviewsSerializer, SafeUserSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleSerializer, UserSerializer)

User = get_user_model()


class ListCreateDestroyMixin(ListModelMixin, CreateModelMixin,
                             DestroyModelMixin,
                             viewsets.GenericViewSet
                             ):
    pass


class CategoryViewSet(ListCreateDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(ListCreateDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [AuthorModerAdmin]

    def get_queryset(self):
        review = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return review.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorModerAdmin]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class SignUp(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            username = request.data.get('username')
            email = request.data.get('email')
            user = get_object_or_404(User, username=username, email=email)

            confirmation_code = default_token_generator.make_token(user)

            user.password = confirmation_code
            user.confirmation_code = confirmation_code
        send_mail(
            'Код подтверждения',
            confirmation_code,
            from_email=None,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainToken(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ObtainTokenSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):

            username = request.data.get('username')
            confirmation_code = request.data.get('confirmation_code')
            serializer.is_valid(raise_exception=True)

            user = get_object_or_404(
                User,
                username=username,
            )

            if user.confirmation_code != confirmation_code:
                return Response(
                    'Confirmation code is invalid',
                    status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response(
                {'access_token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, UserPermissions)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = SafeUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
