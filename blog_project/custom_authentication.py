from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        print("header", header)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception as e:
            raise InvalidToken(f"Token 驗證失敗: {str(e)}")

        user = self.get_user(validated_token)
        if user is None:
            raise AuthenticationFailed('無效使用者', code='user_not_found')

        return (user, validated_token)

    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]
        except KeyError:
            raise InvalidToken("Token 內沒有 user_id")

        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('無此使用者', code='user_not_found')

        return user