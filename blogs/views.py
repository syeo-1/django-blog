from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import BlogPostForm

def check_user_match(blog, request):
    if blog.owner != request.user:
        raise Http404

# Create your views here.
def index(request):
    """home page for blog"""
    blog_posts = BlogPost.objects.order_by('date_added')
    context = {'blog_posts': blog_posts}
    return render(request, 'blogs/index.html', context)

@login_required
def new_post(request):
    """add a new post"""
    if request.method != 'POST':
        # no data submitted ; create a blank form
        form = BlogPostForm
    else:
        # POST data submitted; process the data
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:index')

    # display blank or invalid form
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """edit existing post"""
    post = BlogPost.objects.get(id=post_id)

    check_user_match(post, request)

    if request.method != 'POST':
        # no data submitted ; pre-fill form with existing post
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted; process the data
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')

    # display post with existing data or submit post to edit
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)