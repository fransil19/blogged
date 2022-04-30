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
    success_url =  "/posts"

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

def posts(request):
    posts = Post.objects.all()
    error = ""

    if request.method == "POST":
        post = formPost(request.POST)
        if post.is_valid():

            data = post.cleaned_data
            exist_post = Post.objects.filter(title__icontains=data['title'])

            if len(exist_post)>0 :
                error = "The post already exists"
                post_form = formPost()
                return render(request, 'Blog/posts.html', {"posts": posts,"error": error,"formulario": post_form})

            new_post = Post(title=data['title'],text=data['text'])
            new_post.save()
            post_form = formPost()

            return render(request, 'Blog/posts.html', {"posts": posts,"formulario": post_form})

    else:
        data = request.GET.get('searchtitle', "")
        if data != "":
            searched_posts = Post.objects.filter(title__icontains=data)
            if len(searched_posts)<1 :
                error = "The post doesn't exists"
                post_form = formPost()
                return render(request, 'Blog/posts.html', {"posts": posts,"search_error": error,"formulario": post_form})
            post_form = formPost()
            return render(request, 'Blog/posts.html', {"posts": searched_posts, "formulario": post_form})
        post_form = formPost()
        return render(request, 'Blog/posts.html', {"posts": posts,"formulario": post_form})

""" def users(request):
    users = User.objects.all()
    error = ""

    if request.method == "POST":
        user = formUser(request.POST)
        if user.is_valid():

            data = user.cleaned_data
            exist_user = User.objects.filter(email__icontains=data['email'])

            if len(exist_user)>0 :
                error = "The user already exists"
                user_form = formUser()
                return render(request, 'Blog/users.html', {"users": users,"error": error,"formulario": user_form})

            new_user = User(name=data['name'],surname=data['surname'],email=data['email'])
            new_user.save()
            user_form = formUser()

            return render(request, 'Blog/users.html', {"users": users,"formulario": user_form})

    else:
        data = request.GET.get('searchemail', "")
        if data != "":
            searched_users = User.objects.filter(email__icontains=data)
            if len(searched_users)<1 :
                error = "The user doesn't exists"
                user_form = formUser()
                return render(request, 'Blog/users.html', {"users": users,"search_error": error,"formulario": user_form})
            user_form = formUser()
            return render(request, 'Blog/users.html', {"users": searched_users, "formulario": user_form})
        user_form = formUser()
        return render(request, 'Blog/users.html', {"users": users,"formulario": user_form})
 """
""" def comments(request):
    comments = Comment.objects.all()
    error = ""

    if request.method == "POST":
        comment = formComment(request.POST)
        if comment.is_valid():
            data = comment.cleaned_data
            new_comment = Comment(text=data['text'])
            new_comment.save()
            comment_form = formComment()

            return render(request, 'Blog/comments.html', {"comments": comments,"formulario": comment_form})

    else:
        data = request.GET.get('searchcomment', "")
        if data != "":
            searched_comments = Comment.objects.filter(text__icontains=data)
            if len(searched_comments)<1 :
                error = "The comment doesn't exists"
                comment_form = formComment()
                return render(request, 'Blog/comments.html', {"comments": comments,"search_error": error,"formulario": comment_form})
            comment_form = formComment()
            return render(request, 'Blog/comments.html', {"comments": searched_comments, "formulario": comment_form})
        comment_form = formComment()
        return render(request, 'Blog/comments.html', {"comments": comments,"formulario": comment_form})
 """

def read_posts(request):
    posts = Post.objects.all()

    context = {"posts":posts}

    return render(request, 'Blog/readPosts.html', context)

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()

    posts = Post.objects.all()

    post_form = formPost()
    return render(request, 'Blog/posts.html', {"posts": posts,"formulario": post_form})

def update_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post_form = formPost(request.POST)
        print(post_form)

        if post_form.is_valid:
            data = post_form.cleaned_data

            post.title = data['title']
            post.text = data['text']

            post.save()

            post_form = formPost()
            posts = Post.objects.all()

            return render(request, 'Blog/posts.html', {"posts": posts,"formulario": post_form})
    else:
        post_form = formPost(initial={'title': post.title, 'text': post.text})
        return render(request, 'Blog/updatePost.html', {"post_id":post.id, "formulario": post_form})

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

def delete_avatar(request):
    user = User.objects.get(username=request.user)

    avatar = Avatar.objects.get(user=user)
    avatar.delete()

    return redirect("Profile")