from django.contrib.sitemaps import Sitemap
from .models import Post
#from ..shop.models import Category, Product

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated