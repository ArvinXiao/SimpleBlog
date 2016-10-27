#!/usr/bin/python
#-*-coding:utf-8 -*-
# Set coding. Default coding is ASCII.

from django.shortcuts import render
from django.http import HttpResponse
from models import Article
from datetime import datetime
from django.http import Http404
from django.contrib.syndication.views import Feed #RSS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #slipter page

# Create your views here.
class RSSFeed(Feed):
    title = 'RSS Feed - article'
    link = 'feeds/posts'
    description = 'RSS feed - blog posts'

    def items(self):
        return Article.objects.order_by('-date_time')
    
    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content

# view : home
def home(request):
    articles = Article.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(articles, 2) #每页显示2个

    try:
        article_list = paginator.page(page)
    except PageNotAnInteger :
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.paginator(paginator.num_pages)

    return render(request, 'home.html', {'articles' : article_list})

# view : detail
def details(request, id):
    try:
        article = Article.objects.get(id = str(id))
    except Article.DoesNotExist: #?
        raise Http404

    return render(request, 'details.html', {'article' : article})

def archives(request):
    try:
        articles = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'archives.html', {'articles' : articles, 'error' : False})

def aboutme(request):
    return render(request, 'aboutme.html')

#http://127.0.0.1:8000/tag/highlight/
def categorys(request, category):
    try:
        articles = Article.objects.filter(category__iexact = category)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'categorys.html', {'articles' : articles})

def search(request):
    if 's' in request.GET:
        searchText = request.GET['s']
        if not searchText:
            return render(request, 'home.html')
        else:
            articles = Article.objects.filter(title__icontains = searchText)

            if len(articles) == 0 :
                return render(request, 'archives.html', {'articles' : articles, 'error' : True})
            else:
                return render(request, 'archives.html', {'articles' : articles, 'error' : False})
    return redirect('/')
