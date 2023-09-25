from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
import recipe.views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('edit-profile/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('create/', recipe.views.post_create, name='post_create'),
    path('your-post-list/', recipe.views.post_list, name='post_list'),
    path('search/', recipe.views.SearchResultsView.as_view(), name="search_results"),
    path('ranking/', recipe.views.post_ranking, name='ranking'),
]