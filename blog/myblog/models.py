from django.db import models
#内置用户模型,处理登录注册等
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return '%s' % ( self.name)
class Tag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return '%s' % ( self.name)

class Article(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateField()
    content = models.TextField()
    abstract = models.TextField()
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    tag = models.ManyToManyField(Tag)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
        #主要作用是返回URL
    def get_absolute_url(self):
        # reverse的第一个参数寻找myblog应用下name为detail的函数，reverse会去解析这个函数
        # 对应的URL，第二个参数是文章的主键被传递到URL中去。
        return reverse('myblog:detail',kwargs = {'pk':self.pk})
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    class Meta:
        ordering = ['-time']






