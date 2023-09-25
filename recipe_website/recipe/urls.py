from django.urls import path
from . import views
import account

app_name = 'recipe' 

urlpatterns = [ 
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<slug:post>/<int:year>/<int:month>/<int:day>/', views.post_detail_home, name='post_detail_home'),
    path('rate/', views.rate_post, name='rate_post'),
    path('ranking/', views.post_ranking, name='ranking'),
    path('edit-recipe/<int:post_id>', views.edit, name='edit_recipe'),
    path('delete/<int:post_id>', views.delete, name='delete_recipe'),
]