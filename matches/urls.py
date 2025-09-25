from django.urls import path

from . import views

urlpatterns = [
    path("", views.match_list, name="match_list"),
    path("create/", views.create_match, name="create_match"),
    path("join/<int:match_id>/", views.join_match, name="join_match"),
    path("delete/<int:match_id>/", views.delete_match, name="delete_match"),
    path("update/<int:match_id>/", views.update_match, name="update_match"),
]
