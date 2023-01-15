from django.urls import path

from .views import *

urlpatterns = [
    path('', send_index),
    path('home/', send_index),
    path('login/', Login.as_view()),
    path('register/', Register.as_view()),
    path('note/', NoteSend.as_view()),
    path('note/get/', GetNote.as_view()),
    path('note/delete/<id>', DeleteNote.as_view()),
    path('note/edit/<id>', EditNote.as_view()),
    path('user/<id>', GetUser.as_view())
]