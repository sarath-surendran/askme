from django.urls import path
from .views import *

urlpatterns = [
    path('', homeview, name="home"),
    path('create_questions/',create_question, name='create_question'),
    path("show_question/<int:question_id>/", show_question, name="show_question"),
    path("answer/<int:question_id>/", answer_question, name="answer"),
    path("like/<int:answer_id>/", like, name="like"),
]