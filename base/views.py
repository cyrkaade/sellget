from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Buy, Room, Topic, Message, myUser
from .forms import BuyForm, RoomForm, UserForm, MyUserCreationForm
from django.core.exceptions import ValidationError

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = myUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page':page}
    return render(request, 'base/login_registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_registration.html', {'form':form})

@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(flower_type__name__icontains=q) |
        Q(shade__icontains=q) |
        Q(stock_quantity__icontains=q) |
        Q(price__icontains=q) |
        Q(show_or_no__icontains=q)
        )
    
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__flower_type__name__icontains=q))
    context = {'rooms' : rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}

    if request.user.tier.lower() == 'seller':
        return render(request, 'base/home_for_sellers.html', context)
    else:
        return render(request, 'base/home_for_buyers.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    if request.user.tier.lower() == 'seller':
        return render(request, 'base/room_for_sellers.html', context)
    else:
        return render(request, 'base/room_for_buyers.html', context)


def userProfile(request, pk):
    user = myUser.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    if request.user.tier.lower() == 'seller':
        return render(request, 'base/profile_for_sellers.html', context)
    else:
        return render(request, 'base/profile_for_buyers.html', context)




@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('flower_type')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Buy.objects.create(
            seller = request.user.username,
            quantity = request.POST.get('stock_quantity'),
            quantity_after = request.POST.get('stock_quantity'),
            pricing = request.POST.get('price')
        )
        Room.objects.create(
            host=request.user,
            flower_type=topic,
            shade=request.POST.get('shade'),
            stock_quantity=request.POST.get('stock_quantity'),
            price=request.POST.get('price'),
            show_or_no=request.POST.get('show_or_no'),
            )
        return redirect('home')
    context={'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)




@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('flower_type')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.flower_type = topic
        room.shade=request.POST.get('shade')
        room.stock_quantity=request.POST.get('stock_quantity')
        room.price=request.POST.get('price')
        room.show_or_no=request.POST.get('show_or_no')
        room.save()
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {"form":form})


# @login_required(login_url='login')
# def buyLot(request):
#     # if request.POST:
#     form = BuyForm()

#     if request.method == 'POST':
#         Buy.objects.create(
#             quantity=request.POST.get('quantity'),
#         )
    
#     # if form.is_valid:
#     #     form.save()
#         return redirect('home')    
#     # else:
#     #     form=BuyForm()
#     #     if form.is_valid:
#     #         form.save()

#     return render(request, 'base/buying_form.html', {'form':form})

@login_required(login_url='login')
def buying(request, pk):
    room = Room.objects.get(id=pk)
    buy_item = Buy.objects.get(id=pk)
    form = BuyForm()
    lst = []
    if request.method == 'POST':
        if form.is_valid:
            pill = request.POST.get('quantity')
            user = request.user
            if room.stock_quantity < int(pill):
                raise ValidationError('Higher than maximum amount.')
            # Room.objects.filter(id=pk).update(stock_quantity=F('stock_quantity') - pill)
            buy_item.quantity_after = room.stock_quantity - int(pill)
            buy_item.buyers = buy_item.buyers + user.username + ','
            buy_item.room_revenue = (buy_item.quantity - buy_item.quantity_after) * buy_item.pricing
            buy_item.save()
            room.stock_quantity = room.stock_quantity - int(pill)
            room.save()
            return redirect('home')
    context = {
        'form':form,
        'room':room
    }
    return render(request, 'base/buying_form.html', context)
# @login_required(login_url='login')
# class ItemCreate(CreateView):
#     form_class = BuyForm
#     template_name = 'buying_form.html'
#     success_url = '/thanks/'

#     def get_initial(self):
#         item = get_object_or_404(Buying, pk=self.kwargs['pk'])
#         self.initial.update({
#             'buyer': self.request.user.id,
#             'price': item.price,
#             'item': item.pk,
#         })
#         return super(ItemCreate, self).get_initial()

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})

def get_sum(quantity_before, quantity_after, price):
    return (quantity_before - quantity_after)*price

def script(request):
    buyings = Buy.objects.all()
    total = 0
    rooms = Room.objects.all()
    # for b in buyings:
    #     lst.append(b.room_revenue)
    # total = sum(lst)
    for x in range(0, len(buyings)):
        total += buyings[x].room_revenue
        
        
        # every_lst_sum = (buyings[x].quantity - buyings[x].quantity_after) * buyings[x].pricing
        # buyers_lst = []
    
    context = {
        'rooms':rooms,
        'buyings':buyings,
        'total':total
    }
    return render(request, 'base/script.html', context)


