from django import forms
from .models import Comment

# 要使用表单，先导入forms模块，表单类必须继承自forms.Form类或者forms.ModelForm类。
class CommentForm(forms.ModelForm):
    # 表单的内部类Meta指定和表单相关的数据
    class Meta:
        # 指定这个表单对应的数据库模型为Coments，fields指定需要显示的字段
        model = Comment
        fields = ['name','text']



