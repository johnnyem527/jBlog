from django.db import models
from django.utils import timezone
from django.urls import reverse

'''
Comment Model：
post   Post Model的外键 related_name关联对象反向引用描述符为comments, CASCADE删除方式
author 最大长度为200的字符
text   评论内容
create_date 评论创建时间，默认当前时间
approved_comment 评论是否通过审核的boolean
approve() 评论审核通过，设置approved_comment字段为真，并存入数据库
get_absolute_url() 返回链接地址的绝对路径，此处返回到post列表页
'''
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text