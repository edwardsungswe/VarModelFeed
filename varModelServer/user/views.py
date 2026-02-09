from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import LoginSerializer


class LoginView(APIView):
    """Demo login: validates email + password, returns ok + user_id."""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'ok': False, 'detail': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.password_hash != password:
            return Response(
                {'ok': False, 'detail': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {'ok': True, 'user_id': str(user.id), 'name': user.name},
            status=status.HTTP_200_OK
        )

