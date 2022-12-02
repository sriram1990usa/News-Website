from taggit.models import Tag #import at top
from django.shortcuts import render, get_object_or_404, redirect
from base.models import Category, Article, Comments
from base.forms import CreateArticleForm

from django.core.paginator import Paginator
from django.utils.text import slugify
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect

from django.db.models import Count
from django.contrib import messages
from datetime import date

def index(request):
	categories = Category.objects.filter(active=True)
	featured = Article.objects.filter(status="published", featured=True).order_by("-date")[:8]
	trending_trunc = Article.objects.filter(status="published", trending=True).order_by("-date")[:8]
	trending = Article.objects.filter(status="published", trending=True).order_by("-date")
	top_headlines = Article.objects.filter(status="published", top_headlines=True).order_by("-date")[:3]
	editors_choice = Article.objects.filter(status="published", editors_choice=True).order_by("-date")
	popular = Article.objects.filter(status="published", popular=True).order_by("-date")
	breaking_news = Article.objects.filter(status="published", breaking_news=True).order_by("-date")
	hot = Article.objects.filter(status="published", hot=True).order_by("-date")[:5]
	weekly_favourite = Article.objects.filter(status="published", weekly_favourite=True).order_by("-date")[:6]
	today_headlines = Article.objects.filter(status="published", today_headlines=True).order_by("-date")[:6]

	context = {
		'today_headlines': today_headlines,
		'weekly_favourite': weekly_favourite,
		'hot': hot,
		'breaking_news': breaking_news,
		'popular': popular,
		'editors_choice': editors_choice,
		'top_headlines': top_headlines,
		'trending_trunc': trending_trunc,
		'trending': trending,
		'articles': featured,
		'categories': categories,
	}

	return render(request, 'base/index.html', context)

def articleDetail(request, slug):
	try:
		article = Article.objects.get(slug=slug)
	except:
		article = None
	tags = Tag.objects.all().order_by("?")[:10]
	categories = Category.objects.filter(active=True).order_by("?")

	# Incrementing Article Views
	article.views = article.views + 1
	article.save()

	# All Comments
	comments = Comments.objects.filter(active=True, article=article).order_by("-date")

	# Similar Posts
	post_tags_ids = article.tags.values_list('id', flat=True)
	similar_posts = Article.objects.filter(tags__in=post_tags_ids).exclude(id=article.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-date')[:6]

	context = {
		'categories':categories,
		'article': article,
		'tags': tags,
		'comments': comments,
		'similar_posts':similar_posts,
	}

	return render(request, 'base/article-detail.html', context)

def tag_list(request, tag_slug=None):
    articles = Article.objects.filter(status="published").order_by("-date")

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags__in=[tag])

    return render(request,'base/tags.html',{	'articles':articles, 'tag':tag})

def category(request, category_slug):
    articles = Article.objects.filter(status="published").order_by("-date")
    categories = Category.objects.filter(active=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=category)
        
    # Search Function
    query = request.GET.get("q")
    if query:
        articles = articles.filter(
            Q(title__icontains=query)).distinct()

    # Pagination Function
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    article_paginator = paginator.get_page(page_number)   

    # context for accessing values in templates
    context = {
        'articles': articles,
        'article_paginator': article_paginator,
    }

    return render(request, 'base/category.html', context)


def createArticle(request):
	if request.method == "POST":
		form = CreateArticleForm(request.POST, request.FILES)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.slug = slugify(new_form.title)
			new_form.creator = request.user 
			new_form.save()
			messages.success(request, f'Article Successfully Created, Now in Review.')
			return redirect("/")
	else:
		form = CreateArticleForm()
	context = {
		'form': form,
	}
	return render(request, 'base/create-article.html', context)


# Ajax Sections
def ArticleComment(request, slug):
	article = Article.objects.get(slug=slug)

	# Comment Section
	if request.method == "POST":
		full_name = request.POST.get("full_name")
		email = request.POST.get("email")
		comment = request.POST.get("comment")
		article = Article.objects.get(slug=slug)

		new_comment = Comments.objects.create(full_name=full_name, email=email, comment=comment, article=article)
		new_comment.save()
		response = 'Comment Sent Successfully!'
		return HttpResponse(response)
