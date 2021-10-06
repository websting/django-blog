from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import CommentForm

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
                                
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
        'blog/post/detail.html',
        {'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
        })