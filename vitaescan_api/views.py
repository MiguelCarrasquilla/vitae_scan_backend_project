from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import UserSerializer
from .models import User
from firebase_admin import auth

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("fullname")
        role = data.get("role", "user")
        status_user = data.get("status", "active")
        id_number = data.get("id_number")

        if not email or not password or not full_name or not id_number:
            return Response({"error": "Todos los campos son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crear usuario en Firebase
            firebase_user = auth.create_user(
                email=email,
                password=password,
                display_name=full_name
            )

            user = User.objects.create(
                email=email,
                fullname=full_name,
                id_number=id_number,
                role=role,
                status=status_user
            )

            return Response({
                "message": "Usuario registrado con exito",
                "firebase_user": {
                    "uid": firebase_user.uid,
                    "email": firebase_user.email
                }, "user": {
                    "id": user.id
                }})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def login(self, request):
        id_token = request.data.get("id_token")

        if not id_token:
            return Response({"error": "ID Token es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]

            user = User.objects.get(email=decoded_token.get("email"))

            return Response({
                "message": "Usuario autenticado con exito",
                "firebase_user": {
                    "uid": uid,
                    "email": decoded_token.get("email"),
                    "name": decoded_token.get("name")
                }, "user": {
                    "id": user.id,
                    "email": user.email,
                    "fullname":  user.fullname,
                    "role": user.role,
                    "status": user.status,
                    "id_number": user.id_number,
                }})
        except auth.InvalidIdTokenError:
            return Response({"error": "ID Token es invalido"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "Usuario no registrado"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)