import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    title = 'My blog'
    ### Генерируем URL-адреса
    link = '/blog/'
    #link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog'

    ### Извлекаем включаемые объекты в новостной ленте(последние 5)
    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

    # def item_pubdate(self, item):
    #     return item.publish
