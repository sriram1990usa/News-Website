from base.models import Category
from taggit.models import Tag 


# @login_required
def default(request):
    categories = Category.objects.filter(active=True)
    tags = Tag.objects.all().order_by("?")[:10]



    return{
        'categories':categories,
        'tags':tags,
    }