import io
import time

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .serializers import *
from rest_framework.response import Response
from .models import User, Note
import jwt
from django.conf import settings
import bcrypt
# Create your views here.


reqCounter = 0


def auth_user(data):
    data = jwt.decode(data, settings.SECRET_KEY, algorithms="HS256")
    data = data['name']
    return data

def hash_string(string):
    bytes = string.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    print(hash)
    return hash

def compare_hash_with_string(string, hash):

    string, hash = string.encode('utf-8'), hash.encode('utf-8')

    comparison_status_bool = bcrypt.checkpw(string, hash)
    return comparison_status_bool

class Login(APIView):
    def post(self, request):
        stream = io.BytesIO(request.body)
        json_data = JSONParser().parse(stream)

        user = User.objects.filter(name=json_data['name'])

        if len(user) != 0:
            pswd = user[0].password
            input_password = json_data['password']

            password_correct = compare_hash_with_string(input_password, pswd)

            if password_correct == True:
                encoded_data = jwt.encode({'name': user[0].id}, settings.SECRET_KEY, algorithm="HS256")
                return Response({'token': encoded_data})
            else:
                return Response({'msg': 'Password not correct'})

        else:
            return Response({'msg': "User doesn't exist"})


class Register(APIView):
    def post(self, request):
        stream = io.BytesIO(request.body)
        json_data = JSONParser().parse(stream)

        user = User.objects.filter(name=json_data['name'])
        if len(user) != 0:
            return Response({'msg': 'Not Done'})
        else:
            pswd = json_data['password']
            pswd = hash_string(pswd).decode('UTF-8')
            json_data['password'] = pswd
            user = UserSer(data=json_data)
            print(user)
            if user.is_valid(raise_exception=True):
                user.save()
            return Response({'msg': 'User Registered'})


class NoteSend(APIView):
    def post(self, request):
        stream = io.BytesIO(request.body)
        json_data = JSONParser().parse(stream)
        user = json_data['user']
        user = auth_user(user)
        json_data_2 = {
            'user': user,
            'note': json_data['note']
        }
        note = NoteSer(data=json_data_2)
        if note.is_valid(raise_exception=True):
            note.save()
            return Response({'msg': 'Note sent', 'note': note.data})
        return Response({'msg': 'Note not sent'})


class GetNote(APIView):
    def post(self, request):
        stream = io.BytesIO(request.body)
        json_data = JSONParser().parse(stream)
        user = json_data['name']
        user = auth_user(user)
        note = Note.objects.filter(user_id=user)
        if note is not None:
            response = NoteSer(note, many=True)
            resp = response.data
            resp.reverse()
            return Response({'msg': resp })
        else:
            return Response({'msg': "error"})

class DeleteNote(APIView):
    def post(self, request, id):
        stream = io.BytesIO(request.body)
        json_data = JSONParser().parse(stream)
        user = json_data['name']
        user = auth_user(user)
        id = id
        note = Note.objects.filter(id=id, user=user)
        if note is not None:
            note[0].delete()
            return Response({'msg': 'Deleted', 'id': int(id)})
        else:
            return Response({'msg': 'Object does not exist'})

class EditNote(APIView):
    def post(self, request, id):
        stream = io.BytesIO(request.body)
        json_data = JSONParser().parse(stream)
        user = json_data['name']
        user = auth_user(user)
        id = id

        note = Note.objects.filter(id=id, user=user)
        noteSer = NoteSer(note[0], data=json_data, partial=True)
        if noteSer.is_valid(raise_exception=True):
            noteSer.save()
            return Response({'msg': 'Note Edited', 'note': noteSer.data})
        return Response({'msg': 'Not Done'})

class GetUser(APIView):
    def get(self, request, id):
        id = id
        id = jwt.decode(id, settings.SECRET_KEY, algorithms="HS256")
        user = User.objects.get(id=id['name'])
        if user is not None:
            return Response({'msg': user.name.split(' ')[0]})
        return Response({'msg': 'No account'})


def send_index(request):
    return render(request, 'index.html')
