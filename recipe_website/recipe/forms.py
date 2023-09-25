from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'video', 'status', 
                  'servings', 'ingredients', 'direction_step', 'nutrition_calories', 
                  'nutrition_carbs', 'nutrition_protein', 'nutrition_fat')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'video', 'status', 
                  'servings', 'ingredients', 'direction_step', 'nutrition_calories', 
                  'nutrition_carbs', 'nutrition_protein', 'nutrition_fat')
