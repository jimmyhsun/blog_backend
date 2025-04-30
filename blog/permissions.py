from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrAuthorCanEdit(BasePermission):
    """
    - Admin 可做任何事
    - Author 只能編輯或刪除自己的文章
    - Reader 完全不行（只能看）
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # 允許安全方法（GET, HEAD, OPTIONS）
        if request.method in SAFE_METHODS:
            return True

        # Admin 可以做任何事
        if user.role == 'admin':
            return True

        # Author 只能改自己寫的文章
        if user.role == 'author' and obj.author == user:
            return True

        # 其他（reader或其他情況）不允許
        return False