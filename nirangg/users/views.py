from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken, APIView
from rest_framework_jwt.settings import api_settings
from rest_framework import status

from users.models import NirangUser
from users.serializers import UsersSerializer
from users.basemails import BaseMails

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

UN_AUTHENTICATED_METHODS = ['create']

# Create your views here.


class UsersViewSet(viewsets.ModelViewSet):
    queryset = NirangUser.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (permissions.IsAuthenticated)

    def get_permissions(self):
        if self.action in UN_AUTHENTICATED_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, *args, **kwargs):
        qs = self.queryset.filter(is_deleted=False)
        serializer = self.serializer_class(qs, many=True).data
        return Response(serializer)


    # USER sign up or new user creation
    def create(self, request, *args, **kwargs):
        data = request.data
        data['is_superuser'] = False
        try:
            if 'mobile' in data and data['mobile']:
                data['username'] = data['mobile']
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                serializer_data = serializer.data
                user_data = NirangUser.objects.filter(id=serializer_data['id']).first()
                user_data.set_password(data['password'])
                user_data.save()
                mail = BaseMails()
                mail.send(subject='Account Created', template_name='template.html',
                          recipients=serializer_data['email'],
                          template_data={'username': serializer_data['first_name']})
                return Response(serializer.data, status=Response.status_code)
            else:
                return Response(serializer.errors)
        except Exception as e:
            return Response(e)

    # update user data
    def update(self, request, *args,pk=None, **kwargs):
        user_id = pk
        data = request.data
        try:
            if request.user.id == int(user_id):
                user_queryset = NirangUser.objects.get(id=user_id)
                if 'mobile' in data and data['mobile']:
                    data['username'] = data['mobile']
                serializer = self.serializer_class(user_queryset, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': Response.status_code, 'message': 'success'})
                else:
                    return Response(serializer.errors)
            else:
                return Response({'message': 'Forbidden', 'status':status.HTTP_403_FORBIDDEN})
        except Exception as e:
            return Response(e)

    # delete user
    def destroy(self, request, *args, pk=None, **kwargs):
        user_id = pk
        try:
            # queryset = NirangUser.objects.get(id=user_id)
            queryset = NirangUser.objects.filter(id=user_id)
            if queryset.exists():
                # Soft delete , we usually uses soft delete for history
                queryset.update(deleted=True)
                # command for hard delete
                # queryset.delete()
                return Response({'message': 'success', 'status':status.HTTP_200_OK})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e)


class ObtainJSONWebTokenExtended(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')

            response_data = jwt_response_payload_handler(token, user, request)

            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APILogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

obtain_jwt_token_extended = ObtainJSONWebTokenExtended.as_view()
logout_api = APILogout.as_view()





