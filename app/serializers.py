from rest_framework.serializers import *
from .models import *

class UserSer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "password"]

class NoteSer(ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "user", "note"]