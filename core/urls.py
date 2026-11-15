from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.people_list, name="people_list"),
    path("pessoas/nova/", views.person_create, name="person_create"),
    path("pessoas/<int:pk>/", views.person_detail, name="person_detail"),
    path("pessoas/<int:pk>/editar/", views.person_update, name="person_update"),
    path("pessoas/<int:pk>/atendimentos/novo/", views.attendance_create, name="attendance_create_for_person"),
    path("atendimentos/novo/", views.attendance_create, name="attendance_create"),
]
