from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar', 'dob', 'phone_number',
                  'role']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data["password"])

        user.save()

        return user


class ImageOwnerSerializer(ModelSerializer):
    class Meta:
        model = ImageOwner
        fields = ['image', 'owner']
        extra_kwargs = {'owner': {'required': False}}


class OwnerSerializer(ModelSerializer):
    image_owner = ImageOwnerSerializer(many=True)

    class Meta:
        model = Owner
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'avatar', 'dob', 'phone_number',
                  'role', 'cmt', 'image_owner']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create2(self, validated_data):
        images_data = validated_data.pop('images')
        owner = Owner.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data['avatar'],
            dob=validated_data['dob'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
            cmt=validated_data['cmt']
        )
        o = Owner.objects.get(username=validated_data['username'])
        for image_data in images_data:
            ImageOwner.objects.create(owner_id=o.id, image=image_data)
        return owner


class ImageLodgingSerializer(ModelSerializer):
    class Meta:
        model = ImageLodging
        fields = ['id', 'image', 'lodging']


class SPriceSerializer(ModelSerializer):
    class Meta:
        model = SPrice
        fields = ['id', 'name', 'value', 'lodging']


class LodgingSerializer(ModelSerializer):
    # image_lodging = ImageLodgingSerializer(many=True)
    # service_price = SPriceSerializer(many=True)

    class Meta:
        model = Lodging
        fields = ['id', 'title', 'locate', 'e_price', 'w_price', 'description', 'owner', 'image_lodging',
                  'service_price']

    # def create2(self, validated_data):
    #     images_data = validated_data.pop('image_lodging', [])
    #     service_prices_data = validated_data.pop('service_price', [])
    #     lodging = Lodging.objects.create(**validated_data)
    #
    #     for image_data in images_data:
    #         ImageLodging.objects.create(lodging=lodging, **image_data)
    #
    #     for sprice_data in service_prices_data:
    #         SPrice.objects.create(lodging=lodging, **sprice_data)
    #
    #     return lodging


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'area', 'price', 'content', 'user']
