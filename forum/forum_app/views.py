# forum/views.py
from django.shortcuts import render, get_object_or_404
from .models import Thread

def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', {'threads': threads})

def thread_detail(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    return render(request, 'forum/thread_detail.html', {'thread': thread})
