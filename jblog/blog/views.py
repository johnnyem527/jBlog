from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

# 关于（简单的模板视图）
class AboutView(TemplateView):
    template_name = 'about.html'

'''
博客列表（继承列表视图）
get_queryset() 返回经筛选过的数据集合
field__lookuptype = value ----> __lte = Less than or equal to.
-published_date : descend order 最新的文章放在列表最前面
'''
class PostListView(ListView):
    # default context_object_name is post_list
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

# 博客详情页视图
class PostDetailView(DetailView):
    model = Post

# 创建新博客视图
class CreatePostView(LoginRequiredMixin, CreateView):
    # default template_name = post_form.html
    # default context_object_name = 'post'
    form_class = PostForm
    model = Post

'''
更新博客视图
这里引入了LoginRequiredMixin, 为了确保已经登陆的用户才能更新博文
'''
class PostUpdateView(LoginRequiredMixin, UpdateView):
    # default template_name = post_update_form.html
    # default context_object_name = 'post'
    form_class = PostForm
    model = Post

    def get_queryset(self):
        return Post.objects.all()

# 删除博客
class PostDeleteView(LoginRequiredMixin, DeleteView):
    # default template_name = post_confirm_delete.html
    # default context_object_name = 'post'
    model = Post
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.all()

# 博客草稿
class DraftListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

#######################
#######################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

'''
给博文添加评论的方法
1. 首先需要登陆才能评论
2. 如果是登陆状态，从Model中获取该博文记录
3. 从CommentForm中获得POST提交的form对象
4. 如果form是有效的，将form储存但先不提交
5. 将Model中获取的post赋给form的post外键，关联起来，最后储存该评论
6. 重定向页面到post_detail
7. 否则重回form页面，重新填写form
'''
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            #comment.post外键
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)






















