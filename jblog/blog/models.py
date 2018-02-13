from django.db import models
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

'''
Post Model：
author 外键为django-admin中的注册用户，CASCADE删除方式，外键一般为pk
title  最大长度为200的字符
text   文章内容
create_date 文章创建时间，默认当前时间
published_date 文章发布时间，可以为空
publish() 发布文章时，设置发布日期为当前时间，并储存到数据库
approve_comments() post_list.html统计评论数量
get_absolute_url() 返回链接地址的绝对路径，返回参数为当前文章对象的pk
'''
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    category = models.ForeignKey('blog.Category', default=1, on_delete=models.CASCADE)
    tags = models.ManyToManyField('blog.Tag', blank=True)

    create_date = models.DateTimeField(default=timezone.now)
    modified_date =models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk' : self.pk})

    def __str__(self):
        return self.title

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
