from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Thread, Comment
from django.db.models import Max
from .forms import ThreadForm, CommentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Home View
def home(request):
    boards = Board.objects.all()
    
    data = []
    for board in boards:
        popular = Thread.objects.filter(board=board).order_by('-activity').first()
        data.append({
            "board": board,
            "popular": popular,
        })

    return render(request, 'forum/home.html', {"data": data})

# Boards View
def board_detail(request, short_name):
    board = get_object_or_404(Board, short_name=short_name)

    new_threads = Thread.objects.filter(board=board).order_by('-created_at')[:20]
    popular_threads = Thread.objects.filter(board=board).order_by('-activity')[:10]

    return render(request, 'forum/board_detail.html', {
        "board": board,
        "new_threads": new_threads,
        "popular_threads": popular_threads,
    })

# Create New Thread View
@login_required
def create_thread(request, short_name):
    board = get_object_or_404(Board, short_name=short_name)

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():

            last_id = Thread.objects.aggregate(Max('id'))['id__max'] or 0
            if last_id >= 999:
                return HttpResponse("Max thread ID reached (999).")
            
            thread = form.save(commit=False)
            thread.board = board
            thread.user = request.user
            thread.save()
            return redirect('thread_detail', thread_id=thread.id)
        
    else:
        form = ThreadForm()

    return render(request, 'forum/create_thread.html', {"board": board, "form": form})

# Thread + Create New Comment View
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = Comment.objects.filter(thread=thread).order_by('created_at')

    form = CommentForm()

    return render(request, 'forum/thread_detail.html', {
        "thread": thread,
        "comments": comments,
        "form": form,
    })

@login_required
def create_comment(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    form = CommentForm()
    # comments = Comment.objects.filter(thread=thread).order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.save()

            thread.activity += 1
            thread.save(update_fields=['activity', 'updated_at'])

            return redirect('thread_detail', thread_id=thread.id)
    return redirect('thread_detail', thread_id=thread.id)
