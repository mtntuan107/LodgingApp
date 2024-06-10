from rest_framework.serializers import ModelSerializer
from .models import *
import cloudinary


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "email", "avatar", "dob", "phone_number", "role"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data["password"])

        user.save()

        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url

        return rep


class LodgingSerializer(ModelSerializer):
    class Meta:
        model = Lodging
        fields = ['id', 'active', 'created_date', 'updated_date', 'title', 'locate', 'e_price', 'w_price', 'description'
            , 'owner', 'image_lodging', 'service_price']


