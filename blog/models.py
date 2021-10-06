from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
            self).get_queryset()\
                .filter(status='published')

class Post(models.Model):
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=260)
    slug = models.SlugField(max_length=250, unique_for_date='publish') # to be used in URLs. Short label that contains only letters, numbers, underscores, hyphens.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') # CASCADE = when user is deleted, the db will also delete all its related blog posts.
    image = models.ImageField()
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') # field is related to STATUS_CHOICES above. can be one of two choices only.

    class Meta: # This class contain info. Eg: tells django to sort results by publish field in descendin order.
        ordering = ('-publish',)

    def __str__(self): # default human-readable representation of the object eg: instead of object it will say Comments or Posts etc.
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
            args=[self.publish.year,
                self.publish.month,
                self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'