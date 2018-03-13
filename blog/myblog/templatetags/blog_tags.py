from django.db.models.aggregates import Count
from ..models import Article,Category,Tag
from django import template
# 注册这个函数{% get get_recent_article %}为模版标签，可供模版调用
# 实例化template.Library()类，将函数注册装饰为register.simple_tag模版标签.在模版中就可以通过 {% get_recent_articles %}调用了
register = template.Library()

# 最新文章模版标签
@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('time')[0:num]

# 档案模版标签
@register.simple_tag
def get_archives():
# dates方法返回一个时间列表，月份为单位，降序排列
    return Article.objects.dates('time','month',order='DESC')
# 分类模版标签
@register.simple_tag
def get_category():
    # return Category.objects.all()
    # Count计算分类下的文章数，其接受的参数为需要计数的模型的名称
    # 统计Category记录的集合中每条记录下的与之关联的Post记录的行数，也就是文章数，最后把这个值保存到num_posts属性中。
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.all()
