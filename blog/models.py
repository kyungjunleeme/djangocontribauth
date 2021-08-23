from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag_set = models.ManyToManyField("blog.Tag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(
        # Post, on_delete=models.CASCADE, limit_choices_to={"is_staff": True}
        Post,
        on_delete=models.CASCADE,
    )
    message = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # post_set = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.name
