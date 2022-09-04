from django.urls import path
from base import views


app_name = 'base'

urlpatterns = [

        path('', views.index, name="index"),
        path('create-article', views.createArticle, name="create-article"),

        path('category/<slug:category_slug>', views.category, name="category"),
        path('<slug:slug>', views.articleDetail, name="article-detail"),
        path('<slug:slug>/save-comment/', views.ArticleComment, name="save-comment"),
        path('tag/<slug:tag_slug>/',views.tag_list, name='post_tag'), #
]
