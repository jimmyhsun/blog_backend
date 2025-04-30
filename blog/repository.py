from .models import Post

class PostRepository:
    @staticmethod
    def get_all_posts():
        return Post.objects.all()

    @staticmethod
    def create_post(author, title, content):
        return Post.objects.create(author=author, title=title, content=content)