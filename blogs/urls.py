"""define url patterns for blogs"""

from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # home page
    path('', views.index, name='index'),
    # page for adding new posts
    path('new_post/', views.new_post, name='new_post'),
    # page for editing existing posts
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
]
