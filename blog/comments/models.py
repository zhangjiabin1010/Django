from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    # 在评论是自动创建时间，并在以后可以修改，False为不可修改
    time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('myblog.Article')

    def __str__(self):
        return self.text[:20]
