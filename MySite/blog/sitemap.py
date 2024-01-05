from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    ### Возвращает набор запростов QiueriSet объектов
    def items(self):
        return Post.published.all()

    ### Возвращает время последнего исменения объекта
    def lastmod(self, obj):
        return obj.updated
