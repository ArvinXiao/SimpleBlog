#!/usr/bin/python
#-*-coding:utf-8 -*-
# Set coding. Default coding is ASCII.

from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 100)
    category = models.CharField(max_length = 50, blank = True)
    date_time = models.DateTimeField(auto_now_add = True)
    content = models.TextField(blank = True, null = True)
    author = models.CharField(max_length = 100, null = True)

    def __unicode__(self):
        return self.title

    class Meta: #按时间下降排序
        ordering = ['-date_time']

    def get_absolute_url(self):
        path = reverse('details', kwargs={'id' : self.id})
        return 'http://127.0.0.1:8000%s' % path;