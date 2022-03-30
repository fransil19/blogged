from xmlrpc.client import DateTime
from django.shortcuts import render
from django.http import HttpResponse
from Blog.models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'Blog/index.html')

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


def users(request):
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


def comments(request):
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



    