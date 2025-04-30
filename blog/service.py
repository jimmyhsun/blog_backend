from .repository import PostRepository

class PostService:
    @staticmethod
    def list_posts():
        return PostRepository.get_all_posts()

    @staticmethod
    def create_post(author, title, content):
        return PostRepository.create_post(author, title, content)