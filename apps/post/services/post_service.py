from django.http import Http404

from apps.post.models.post_models import HashTagModel, Post, PostFileModel


class PostService:
    @staticmethod
    def create_post(owner, description, location, tagged_users=None, hashtags=None, files=None):
        # if not files:
        #     raise ValueError("Files are required for creating a post")

        post = Post.objects.create(owner=owner, description=description, location=location)

        # Создание хэштегов, если они указаны
        if hashtags:
            for tag_name in hashtags:
                hashtag, _ = HashTagModel.objects.get_or_create(name=tag_name)
                post.hashtags.add(hashtag)

        # Создание файлов, если они указаны
        if files:
            for file_data in files:
                PostFileModel.objects.create(post=post, file=file_data)

        # Привязка пользователей к посту, если они указаны
        if tagged_users:
            post.tagged_users.set(tagged_users)

        return post

    @staticmethod
    def _update_hashtags(post, hashtags):
        if hashtags:
            post.hashtags.clear()  # Очищаем текущие хэштеги
            for tag_name in hashtags:
                hashtag, _ = HashTagModel.objects.get_or_create(name=tag_name)
                post.hashtags.add(hashtag)

    @staticmethod
    def update_post(post_id, validated_data):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")

        # Обновление данных поста
        post.description = validated_data.get("description", post.description)
        post.location = validated_data.get("location", post.location)

        # Обновление хэштегов
        hashtags = validated_data.get("hashtags")
        PostService._update_hashtags(post, hashtags)

        post.save()

        return post

    @staticmethod
    def partial_update_post(post_id, validated_data):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")

        # Частичное обновление данных поста
        if "description" in validated_data:
            post.description = validated_data["description"]
        if "location" in validated_data:
            post.location = validated_data["location"]

        # Обновление хэштегов
        hashtags = validated_data.get("hashtags")
        PostService._update_hashtags(post, hashtags)

        post.save()

        return post

    @staticmethod
    def delete_post(post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")

        post.delete()
