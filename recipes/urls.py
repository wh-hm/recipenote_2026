
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("recipes/", views.recipe_list_view, name="recipe_list"),
    path(
        "recipes/<int:recipe_id>/",
        views.recipe_detail_view,
        name="recipe_detail"
    ),
    path(
        "recipes/create/",
        views.recipe_create_view,
        name="recipe_create"
    ),
    path(
        "recipes/<int:recipe_id>/image/",
        views.recipe_image_view,
        name="recipe_image"
    ),

    # レシピ編集
    path(
        "recipes/<int:recipe_id>/edit/",
        views.recipe_edit_view,
        name="recipe_edit"
    ),

    # レシピ削除
    path(
        "recipes/<int:recipe_id>/delete/",
        views.recipe_delete_view,
        name="recipe_delete"
    ),
]
