from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import User, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PostModelForm, editForm


def logoutUser(request):
    logout(request)
    return redirect('login')


# ********************************************************************

@login_required(login_url='login')
def home(request):
    user = request.user
    print('user is', user.id)
    showPost = Post.objects.all().order_by('-id')
    return render(request, "posts/home.html", {"showPost": showPost})


@login_required(login_url='login')
def addPost(request):
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.createdby_id = request.user.pk
        instance.img = request.user.username
        instance.save()
        return redirect("home")
    return render(request, "posts/addPost.html", {"form": form})


@login_required(login_url='login')
def ParticularPost(request, id):
    print("inside particular q id is", id)
    p = Post.objects.get(id=id)
    img = "https://images4.alphacoders.com/722/722452.png"
    return render(request, 'posts/ParticularPost.html', {"post": p, "img": img})

# Share via email


@login_required(login_url='login')
def myPost(request):
    my_post = Post.objects.filter(createdby_id=request.user.pk)
    print(myPost)
    return render(request, 'posts/myPost.html', {"myPost": my_post, 'user': request.user.id})


@login_required(login_url='login')
def editPost(request, id):
    p = Post.objects.get(id=id)
    form = editForm(instance=p)

    if request.method == 'POST':
        form = editForm(request.POST, request.FILES, instance=p)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/home/')

    context = {'form': form, 'post': p, 'userId': request.user.id}
    return render(request, 'posts/editPost.html', context)


@login_required(login_url='login')
def delPost(request, id):
    p = Post.objects.get(id=id)

    if request.method == 'POST':
        p.delete()
        return redirect('/home/')

    context = {'post': p, 'user': request.user}
    return render(request, 'posts/delete.html', context)


def post_search(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Post.objects.filter(title__icontains=search_query).filter(
                description__icontains=search_query).distinct()
            context['showPost'] = search_results

    print("----------------------------------------------------------------------------")
    print(context)
    return render(request, "posts/search_results.html", context)
