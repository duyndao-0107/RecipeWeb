from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils.text import slugify 

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = ( ('draft', 'Draft'), ('published', 'Published'), )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_posts')
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/image/%Y/%m/%d/', blank=True)
    video = models.FileField(upload_to='posts/video/%Y/%m/%d/', blank=True)
    url = models.URLField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    score = models.IntegerField(default=0, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    servings = models.IntegerField(default=0)
    ingredients = models.TextField(blank=True)
    direction_step = models.TextField(blank=True)
    nutrition_calories = models.IntegerField(default=0)
    nutrition_carbs = models.IntegerField(default=0)
    nutrition_protein = models.IntegerField(default=0)
    nutrition_fat = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        
        super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recipe:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
    def get_absolute_url_home(self):
        return reverse('recipe:post_detail_home', args=[ self.slug, self.publish.year, self.publish.month, self.publish.day])
    
    def get_absolute_url_edit_recipe(self):
        return reverse('recipe:edit_recipe', args=[self.id,])
    
    def get_absolute_url_delete_recipe(self):
        return reverse('recipe:delete_recipe', args=[self.id,])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
