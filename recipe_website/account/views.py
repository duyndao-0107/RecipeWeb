from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, EmailPostForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from recipe.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from images.models import Image
from django.core.mail import send_mail
from django.contrib.auth.models import User

def home(request):
    object_list = Post.published.all()
    
    images = Image.objects.all()
    
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

    return render(request, 'account/home.html', {'section': 'home', 
                                                 'posts': posts, 
                                                 'images': images})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password( user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            
            # Create the user profile
            Profile.objects.create(user=new_user)
            
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
            
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid ():
            user_form.save()
            
            profile_form.save()

            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect("/recipe/")
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        
        profile_form = ProfileEditForm(instance=request.user.profile)
            
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

def pw_reset_for_email(request, username=None):
    # Retrieve post by id
    user = User.objects.get(email=username)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            # user_url = request.build_absolute_uri({{ protocol }}://{{ domain }})
            subject = f"Someone asked for password reset for email " f"{cd['email']}" f"{cd['username']}"
            message = f"Follow the link below:\n \n\n" "Your username, in case you've forgotten: " f"{cd['username']}"
            send_mail(subject, message, 'recipe@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'registration/password_reset_confirm.html', {'form': form,
                                                                        'sent': sent})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    
    return render(request, 'account/user/list.html', {'section': 'people', 
                                                      'users': users})
