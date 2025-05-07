from rest_framework import serializers
from .models import Comment, Ad


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source="author.first_name", read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", read_only=True)
    author_image = serializers.CharField(source="author.image", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, default=None)

    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'image', 'title', 'price', 'description', 'author']

    def get_author(self, obj):
        return {
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
            'phone': obj.author.phone
        }
