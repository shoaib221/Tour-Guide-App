from django.urls import path, include
from . import views
from django.urls import  include, re_path

urlpatterns = [
    path('', views.blog, name='blog'),
    # path('', views.new_post.as_view(), name='newpost'),
    path('newpost/', views.new_post, name='newpost'),
    # url(r'^newpost(?P<pk>[0-9]+)/$', views.new_post, name='newpost'),
    path('bloglist/', views.PostList, name='bloglist'),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    # path('<int:id>/', views.PostDetail, name='post_detail'),
    # path()
    
    re_path(r'^bloglist/(?P<pk>[0-9]+)/$',
        views.PostDetail.as_view(), name='post_detail'),
    re_path(r'^bloglist/(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$',
        views.PostPreference, name='postpreference'),
    # url(r'^like/(?P<pk>[0-9]+)/$', views.like_post, name='like_post'),
    # path('like/', views.like_post, name='like_post'),
    re_path(r'^blogist/(?P<pk>[0-9]+)/edit/$',
        views.UpdatePost.as_view(), name='post_edit'),
    re_path(r'^bloglist/(?P<pk>[0-9]+)/remove/$',
        views.DeletePost.as_view(), name='post_remove'),



    re_path(r'^bloglist/(?P<pk>[0-9]+)/approve/$',
        views.comment_approve, name='comment_approve'),
    re_path(r'^bloglist/(?P<pk>[0-9]+)/remove/$',
        views.comment_remove, name='comment_remove'),

    re_path(r'^bloglist/(?P<pk>[0-9]+)/comment/$',
        views.addComment, name='addcomment'),


]
