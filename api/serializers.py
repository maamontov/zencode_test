from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Image, Comment, Like


User = get_user_model()


# region help
class CurrentImageDefault:
    requires_context = True

    def __call__(self, serializer_field):
        image_pk = serializer_field.context['request'].parser_context[
            'kwargs']['image_pk']
        return Image.objects.get(pk=image_pk)


class WithUserImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.HiddenField(default=CurrentImageDefault())


class WithCountersSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    @staticmethod
    def get_likes_count(obj):
        return obj.likes_count

    @staticmethod
    def get_comments_count(obj):
        return obj.comments_count
# endregion


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class ImageCreateUpdateDestroySerializer(WithCountersSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Image
        fields = '__all__'


class ImageSerializer(WithCountersSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class CommentCreateUpdateDestroySerializer(WithUserImageSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ['image']


class LikeCreateDestroySerializer(WithUserImageSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'image'),
                message='Image already rated.'
            )
        ]


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        exclude = ['id', 'image']
