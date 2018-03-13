from django.shortcuts import render,get_object_or_404,redirect
from myblog.models import Article
from .models import Comment
from .forms import CommentForm
# 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
# 当获取的文章存在时，则获取；否则返回 404
def article_comment(request,article_pk):
    article = get_object_or_404(Article,pk = article_pk)
    if request.method == 'POST':
        # 获取到的数据存在request.POST中，这是一个类字典对象。
        # 利用这些数据构造CommentForm的实例，表单就生成了
        form = CommentForm(request.POST)
        # 检查到数据是合法的，保存数据到数据库
        if form.is_valid():
            # 将表单数据生成为Comments模型类的实例，但还不提交到数据库
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            # 重定向到文章详情页。当redirect函数接收到一个模型的实例时
            # 自动调用实例的get_absolute_url方法返回的URL
            return redirect(article)
        else:
            # 如果检测到数据不合法，重新渲染文章页，渲染表单错误。将3个模版变量传给detail.html
            # 因为Post和Comment是ForeignKey关联的,
            # 因此使用post.comment_set.all()反向查询全部评论

            # 获取和article关联的评论列表，调用它的xxx(关联模型的类名，小写)_set属性来获取类似于object的模型管理器
            # 然后调用其all方法，返回这个article关联的评论。例如 Article.objects.filter(category=cate) 也可以等价写为 cate.article_set.all()。
            comment_list = article.comment_set.all()
            context = {
                'article':article,
                'form':form,
                'comment_list':comment_list
            }
            return render(request,'blog/detail.html',context=context)
        # 不是post请求，就重定向到文章详情页
        return redirect(article)
