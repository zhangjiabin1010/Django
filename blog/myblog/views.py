from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from .models import Article,Category,Tag
from comments.forms import CommentForm
from django.db.models import Q
import markdown

# 以下为传统首页视图
# def index(request):
    # article_list = Article.objects.all()
    # return render(request,'blog/index.html',context={'article_list':article_list})

# 类视图函数：特用于从数据库中获取某个模型列表数据
class IndexView(ListView):
    # 获取模型为Article
    model = Article
    # 渲染页面
    template_name = 'blog/index.html'
    # 获取到的模型列表数据，保存给变量。
    context_object_name = 'article_list'
    #分页
    paginate_by = 4

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context


    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# def detail(request, pk):
#     # get_object_or_404(),当传入的pk值对应的Article在数据库存在，就返回对应的article，不存在就返回404
#     article = get_object_or_404(Article, pk=pk)
#     # 对文章的内容进行Markdown渲染，把 markdown文本转为html文本再传给模版
#     article.content = markdown.markdown(article.content, extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     # 阅读量
#     article.increase_views()
#     # 评论
#     form = CommentForm()
#     comment_list = article.comment_set.all()
#     context = {
#         'article': article,
#         'form': form,
#         'comment_list': comment_list
#     }
#
#     return render(request, 'blog/detail.html', context=context)
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    # 覆写get方法，当文章被访问一次，阅读量 +1。get方法返回的是HttpResponse实例,之所以调用父类的get方法，是因为
    # 当get方法被调用后，才有 self.object属性，其值为Article模型实例，即被访问的文章article。

    #get方法就相当于一个detail视图函数。下面的两个函数是辅助函数，最后在get方法中被调用，看不到它们被调用的原因是它们
    # 隐含在super(ArticleDetailView,self).get()方法的调用中，返回的response,就是get方法返回的HttpResponse对象
    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        return response

    # 覆写 get_object 方法的目的是因为需要对 article 的 body 值进行渲染。
    def get_object(self, queryset=None):
        article = super(ArticleDetailView,self).get_object(queryset=None)
        # 没有直接用markdown.markdown()方法来渲染post.body中的内容，而是先实例化了一个markdown.Markdown类md
        # 使用该实例的convert方法将article.content中的Markdown文本渲染成HTML文本,调用这个方法后，实例md会多出一个toc属性
        # 属性的值就是内容的目录,把md.toc的值赋给 article.toc 属性，article本来是没有这个属性的，这是动态添加的md属性
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        article.content = md.convert(article.content)
        article.toc = md.toc
        return article

    # 覆写get_context_data的目的是因为除了将article传递给模板外（DetailView已经帮我们完成）
    #     还要把评论表单，评论列表传递给模版，返回的值是一个模版变量字典，最终传递给模版
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,'comment_list':comment_list
        })
        return context
# 分类
# def category(request,pk):
#     category = get_object_or_404(Category,pk=pk)
#     article_list = Article.objects.filter(category=category)
#     return render(request,'blog/index.html',context={'article_list':article_list})
# 分类 类视图
class CategoryView(ListView):
    # 分类列表依然要从文章article模型里拿数据
    model = Article
    template_name = 'blog/index.html'
    # 取到的模型数据仍然保存到article_list里
    context_object_name = 'article_list'
    # 获取到全部数据之后，还需要从url中捕获分类ID，并从数据库获取分类下的文章
    # 覆写父类的get_quaryset方法，该方法默认获取模型全部列表，为了获取指定分类下列表，我们覆写方法，改变默认行为
    # 因为上面三句和IndexView类里属性值一样吗，所以下面的def get_queryset(IndexView):可以直接取代上面三句属性值
    def get_queryset(self):
        # 捕获PK值获取分类，将捕获的命名组参数值保存到kwargs（是一个字典）属性，非命名组的参数值保存到args（列表）属性，
        # 所以这里我们用self.kwargs0.get('pk')获取分类id值。
        category = get_object_or_404(Category,pk = self.kwargs.get('pk'))
        # 调用父类的get_queryset方法获得全部文章列表后，对返回结果调用filter方法，筛选后返回
        return super(CategoryView, self).get_queryset().filter(category = category)


# 归档 函数视图 和 类视图
# def archives(request,year,month):
#     article_list = Article.objects.filter(
#         time__year=year,
#         time__month=month
#     )
#     return render(request,'blog/index.html',context={'article_list': article_list})
# 归档 函数视图 和 类视图
class ArchivesView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(time__year = year,
                                                                time__month = month)


# 标签云
def tag(request,pk):
    tag = get_object_or_404(Tag,pk=pk)
    article_list = Article.objects.filter(tag=tag)
    return render(request,'blog/index.html',context={'article_list':article_list})

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    article_list = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'article_list': article_list})
def contact(request):
    return render(request,'blog/contact.html')



