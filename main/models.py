from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=99, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description


class Cart(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=99, null=False, blank=False)

    def __str__(self):
        return self.author.username+"@@"+self.post.title
    
class Order(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=99, null=False, blank=False)
    address = models.CharField (max_length=50, default='', blank=True)
    phone = models.CharField (max_length=50, default='', blank=True)
    created_at = models.DateTimeField()
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.author.email
    
    
class MyOrders(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    author_id = models.IntegerField(max_length=50, blank=False, null=False)
    author_name = models.CharField(max_length=50, blank=False, null=False)
    author_email = models.CharField(max_length=50, blank=False, null=False)

    post_id = models.IntegerField(max_length=50, blank=False, null=False)
    post_title = models.CharField(max_length=50, blank=False, null=False)
    post_desc = models.TextField()
    post_amount = models.DecimalField(max_digits=9, decimal_places=2, default=99, null=False, blank=False)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=99, null=False, blank=False)    