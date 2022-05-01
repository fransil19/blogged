from django.shortcuts import get_list_or_404, render,redirect
from django.http import HttpResponseRedirect
from Blog.models import *
from .forms import *

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

#For Login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

#decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostList(ListView):
    model = Post
    template_name = "Blog/post_list.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if(self.request.user.is_authenticated):
            avatar = Avatar.objects.filter(user = self.request.user)
            if avatar:
                image = avatar[0].image.url
                context['avatar'] = image
        return context


class PostFilterList(ListView):
    model = Post
    template_name = "Blog/post_list.html"

    def get_queryset(self):
        return get_list_or_404(Post, title__icontains= self.kwargs['searchtitle'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if(self.request.user.is_authenticated):
            avatar = Avatar.objects.filter(user = self.request.user)
            if avatar:
                image = avatar[0].image.url
                context['avatar'] = image
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "Blog/post_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if(self.request.user.is_authenticated):
            avatar = Avatar.objects.filter(user = self.request.user)
            if avatar:
                image = avatar[0].image.url
                context['avatar'] = image
        return context

    @method_decorator(login_required(redirect_field_name='my_redirect_field'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    success_url = "/pages"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if(self.request.user.is_authenticated):
            avatar = Avatar.objects.filter(user = self.request.user)
            if avatar:
                image = avatar[0].image.url
                context['avatar'] = image
        return context

    """ def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PostCreate, self).form_valid(form) """
    
    @method_decorator(login_required(login_url='/accounts/login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    success_url =  "/pages"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if(self.request.user.is_authenticated):
            avatar = Avatar.objects.filter(user = self.request.user)
            if avatar:
                image = avatar[0].image.url
                context['avatar'] = image
        return context

class PostDelete(DeleteView):
    model = Post
    success_url =  "/pages"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if(self.request.user.is_authenticated):
            avatar = Avatar.objects.filter(user = self.request.user)
            if avatar:
                image = avatar[0].image.url
                context['avatar'] = image
        return context
    
# Create your views here.
def index(request):
    if(request.user.is_authenticated):
        avatar = Avatar.objects.filter(user = request.user)
        if avatar:
            image = avatar[0].image.url
            return render(request, 'Blog/index.html', {"avatar": image})
    return render(request, 'Blog/index.html')

def about(request):
    if(request.user.is_authenticated):
        avatar = Avatar.objects.filter(user = request.user)
        if avatar:
            image = avatar[0].image.url
            return render(request, 'Blog/about.html', {"avatar": image})
    return render(request, 'Blog/about.html')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                return render(request, "Blog/index.html", {"message": f"Welcome {username}"})
            else:
                return render(request, "Blog/index.html", {"message": f"Error, incorrect username/password"})
        else:
            return render(request, "Blog/index.html", {"message": f"Error, form with errors"})
    form = AuthenticationForm()

    return render(request, "Blog/login.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            return redirect("Index")

    else:
        form = UserRegisterForm()

    return render(request, "Blog/register.html", {"form": form})

@login_required
def editProfile(request):
    user = request.user

    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user.email = data["email"]
            user.username = data["username"]
            user.password1 = data["password1"]
            user.password2 = data["password2"]

            user.save()

            return redirect("Index")

    else:
        form = UserEditForm(initial={"email":user.email, "username":user.username})

        avatar = Avatar.objects.filter(user = request.user)
        if avatar:
            image = avatar[0].image.url
            return render(request, "Blog/edit_profile.html", {"form":form, "user":user,"avatar": image})

    return render(request, "Blog/edit_profile.html", {"form":form, "user":user})

@login_required
def addAvatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(username=request.user)
            try:
                avatar = Avatar.objects.get(user = user)
                avatar.image = form.cleaned_data["image"]
            except:
                avatar = Avatar(user=user, image=form.cleaned_data["image"])
                return redirect("Index")
            finally:
                avatar.save()
                return redirect("Index")    
    else:
        form = AvatarForm()
    
    return render(request,"Blog/addAvatar.html", {"form":form})

@login_required
def delete_avatar(request):
    user = User.objects.get(username=request.user)

    avatar = Avatar.objects.get(user=user)
    avatar.delete()

    return redirect("Profile")