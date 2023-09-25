from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm, PostCreateForm, PostEditForm, UserCreateForm
from images.models import Image
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from django.db.models import Q
import redis
from django.conf import settings
from django.contrib.auth.models import User

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST, 
                port=settings.REDIS_PORT, 
                db=settings.REDIS_DB)

@login_required
def post_list(request):
    object_list = Post.objects.filter(author_id=request.user.id, status= "published")

    paginator = Paginator(object_list, 6)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
        
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'recipe/post/list.html', {'posts': posts,
                                                     'page': page})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                             status='published', 
                             publish__year=year, 
                             publish__month=month, 
                             publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    # increment total post views by 1
    total_views = r.incr(f'post:{post.id}:views')

    # increment post ranking by 1
    r.zincrby('post_ranking', 1, post.id)
    
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)

            comment_form.instance.name = request.user

            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    # obj = Post.objects.filter(score=0).order_by("?").first()
    
    return render(request, 'recipe/post/detail.html', {'post': post,
                                                       'comments': comments, 
                                                       'new_comment': new_comment, 
                                                       'comment_form': comment_form,
                                                       'total_views': total_views})

def post_detail_home(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                             status='published', 
                             publish__year=year, 
                             publish__month=month, 
                             publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    # increment total post views by 1
    total_views = r.incr(f'post:{post.id}:views')

    # increment post ranking by 1
    r.zincrby('post_ranking', 1, post.id)
    
    return render(request, 'account/detail.html', {'post': post,
                                                   'comments': comments,
                                                   'total_views': total_views})

@login_required
def post_create(request):
    if request.method == 'POST':
        post_form = PostCreateForm(data=request.POST, files=request.FILES)        
        
        if post_form.is_valid ():
            post_form.save(commit=False)

            post_form.instance.author = request.user

            post_form.save()

            messages.success(request, 'Post updated successfully')

            return HttpResponseRedirect("/menu/")
        else:
            messages.error(request, 'Error updating your profile')
       
    else:
        post_form = PostCreateForm(data=request.GET)
            
    return render(request, 'recipe/post/create.html', {'post_form': post_form})

@login_required
def rate_post(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        # action = request.POST.get('action')
        
        val = request.POST.get('val')
        obj = Post.objects.get(id=el_id)
        obj.score = val
        obj.save()
        
        return JsonResponse({'success': 'true', 'score': val}, safe=False)
    
    return JsonResponse({'success': 'false'})

class SearchResultsView(ListView):
    model = Post
    template_name = 'recipe/post/search.html'

    def get_queryset(self):
        query = self.request.GET.get("q")

        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

        return object_list

@login_required
def post_ranking(request):
    # get post ranking dictionary
    post_ranking = r.zrange('post_ranking', 0, -1, desc=True)[:10]
    post_ranking_ids = [int(id) for id in post_ranking]
    # get most viewed images
    most_viewed = list(Post.objects.filter(id__in=post_ranking_ids))
    most_viewed.sort(key=lambda x: post_ranking_ids.index(x.id))
    
    return render(request, 'recipe/post/ranking.html', {'section': 'posts',
                                                        'most_viewed': most_viewed})

@login_required
def edit(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post_form = PostEditForm(instance=post, data=request.POST, files=request.FILES)
        
        if post_form.is_valid ():
            post_form.save()

            return HttpResponseRedirect('/menu/')

            # messages.success(request, 'Post updated successfully')
            # return HttpResponseRedirect("/your-post-list/")
        else:
            messages.error(request, 'Error updating your post')
    else:
        post_form = PostEditForm(instance=post)
            
    return render(request, 'recipe/post/edit.html', {'post': post,
                                                     'post_form': post_form})

@login_required
def delete(request, post_id=None):
    post_to_delete=Post.objects.get(id=post_id)
    post_to_delete.delete()

    return HttpResponseRedirect('/menu/')