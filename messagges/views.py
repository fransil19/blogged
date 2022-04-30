from django.shortcuts import get_list_or_404, render,redirect
from .models import *
from .forms import *
from Blog.models import Avatar

from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def messages(request):
    criterio1 = Q(user_to=request.user)
    criterio2 = Q(user_from=request.user)
    messages = Message.objects.filter(criterio1 | criterio2)
    users = []

    for message in messages:
        if message.user_from.id != request.user.id:
            users.append(message.user_from)
    users = list(set(users))

    avatar = Avatar.objects.filter(user = request.user)
    if avatar:
        image = avatar[0].image.url
        return render(request, 'messagges/messages.html', {"users":users,"avatar": image})

    return render(request, 'messagges/messages.html', {"users":users})

def messages_with(request, id):
    user = User.objects.get(id = id)
    criterio1 = Q(user_to=request.user)
    criterio2 = Q(user_from=user)
    criterio3 = Q(user_from=request.user)
    criterio4 = Q(user_to=user)

    messages = Message.objects.filter((criterio1 & criterio2) | (criterio3 & criterio4)).order_by("date")

    if request.method == "POST":
        message = MessageForm(request.POST)
        if message.is_valid():

            data = message.cleaned_data

            new_message = Message(text=data['text'],user_from=request.user, user_to=user)
            new_message.save()
            message_form = MessageForm()

            avatar = Avatar.objects.filter(user = request.user)
            if avatar:
                image = avatar[0].image.url
                return render(request, 'messagges/messages_with.html', {"messages": messages,"formulario": message_form,"avatar": image})

            return render(request, 'messagges/messages_with.html', {"messages": messages,"formulario": message_form})
    else:
        message_form = MessageForm()
        avatar = Avatar.objects.filter(user = request.user)
        if avatar:
            image = avatar[0].image.url
            return render(request, 'messagges/messages_with.html', {"messages": messages,"formulario": message_form,"user":user,"avatar": image})
        return render(request, 'messagges/messages_with.html', {"messages": messages,"formulario": message_form,"user":user})


def create_message(request):

    if request.method == "POST":
        message = NewMessageForm(request.POST)
        if message.is_valid():

            data = message.cleaned_data
            user_to = User.objects.get(id = data['user_to'].id)

            new_message = Message(text=data['text'],user_from=request.user, user_to=user_to)
            new_message.save()
            message_form = NewMessageForm()

            return redirect("MessagesWith",id=user_to.id)
    else:
        message_form = NewMessageForm()
        avatar = Avatar.objects.filter(user = request.user)
        if avatar:
            image = avatar[0].image.url
            return render(request, 'messagges/new_message.html', {"messages": messages,"formulario": message_form,"avatar": image})
        return render(request, 'messagges/new_message.html', {"messages": messages,"formulario": message_form})