from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .paginator import *
from django.shortcuts import get_object_or_404


def index(request):
    return HttpResponse("app find lodging")


def test(request, x):
    return HttpResponse("Hello" + str(x))


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(UserSerializer(user).data)

    @action(detail=True, methods=['post'], url_path='create-post')
    def create_post(self, request, pk=None):
        user = self.get_object()  # Get the owner instance
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Set the owner field before saving
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerCreateViewSet(viewsets.ModelViewSet,
                         generics.ListAPIView,
                         generics.CreateAPIView,
                         generics.RetrieveAPIView,
                         generics.DestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    parser_classes = [MultiPartParser, ]

    @action(methods=['get', 'patch'], url_path='current-owner', detail=False)
    def get_current_owner(self, request):
        try:
            owner = Owner.objects.get(id=request.user.id)
        except Owner.DoesNotExist:
            return Response({"detail": "Not an owner."}, status=400)

        if request.method == 'PATCH':
            for k, v in request.data.items():
                setattr(owner, k, v)
            owner.save()

        return Response(OwnerSerializer(owner).data)

    @action(detail=True, methods=['post'], url_path='create-lodging')
    def create_lodging(self, request, pk=None):
        owner = self.get_object()  # Get the owner instance
        serializer = LodgingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)  # Set the owner field before saving
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='follow', detail=True)
    def follow(self, request, pk):
        follow, created = Follow.objects.get_or_create(owner=self.get_object(),
                                                       user=request.user)
        if not created:
            follow.active = not follow.active
            follow.save()

        return Response(AuthenticatedOwnerDetailsSerializer(self.get_object()).data)


class LodgingViewSet(viewsets.ModelViewSet):
    queryset = Lodging.objects.filter(active=True)
    serializer_class = LodgingSerializer
    # permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, ]
    # pagination_class = LodgingPaginator

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(methods=['get'], url_path='comment_ul', detail=True)
    def get_comment_ul(self, request, pk):
        comment_ul = self.get_object().comment_set.select_related('user').order_by('-id')

        paginator = CommentPaginator()
        page = paginator.paginate_queryset(comment_ul, request)
        if page is not None:
            serializer = CommentULSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(CommentULSerializer(comment_ul, many=True).data)

    @action(methods=['post'], url_path='comment_ul', detail=True)
    def add_comment_ul(self, request, pk):
        c_ul = self.get_object().comment_set.create(content=request.data.get('content'),
                                                    user=request.user)
        return Response(CommentSerializer(c_ul).data, status=status.HTTP_201_CREATED)

# class ImageOwnerViewSet(viewsets.ModelViewSet, generics.CreateAPIView,
#                         generics.RetrieveAPIView, generics.ListAPIView):
#     queryset = ImageOwner.objects.all()
#     serializer_class = ImageOwnerSerializer
#
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]


# class ImageLodgingViewSet(viewsets.ModelViewSet, generics.CreateAPIView,
#                         generics.RetrieveAPIView, generics.ListAPIView):
#     queryset = ImageLodging.objects.all()
#     serializer_class = ImageLodgingSerializer
#
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]


# class SPriceViewSet(viewsets.ModelViewSet, generics.CreateAPIView,
#                         generics.RetrieveAPIView, generics.ListAPIView):
#     queryset = SPrice.objects.all()
#     serializer_class = SPriceSerializer
#
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]


class PostViewSet(viewsets.ModelViewSet, generics.CreateAPIView,
                  generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]

    @action(methods=['get'], url_path='comment', detail=True)
    def get_comment(self, request, pk):
        comment = self.get_object().comment_set.select_related('owner').order_by('-id')

        paginator = CommentPaginator()
        page = paginator.paginate_queryset(comment, request)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(CommentSerializer(comment, many=True).data)

    @action(methods=['post'], url_path='comment', detail=True)
    def add_comment(self, request, pk):
        c = self.get_object().comment_set.create(content=request.data.get('content'),
                                                 owner=request.owner)
        return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Follow.objects.filter(user=self.request.user)
        return Follow.objects.none()

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(methods=['post'], url_path='follow', detail=True)
    def follow(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        owner = get_object_or_404(Owner, pk=pk)
        follow, created = Follow.objects.get_or_create(user=request.user, owner=owner)
        if created:
            return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)
        follow.delete()
        return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)

