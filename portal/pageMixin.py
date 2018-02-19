from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PaginatorGenerator(object):

    def page(self, materials):
        page = self.request.GET.get('page')
        paginator = Paginator(self.materials, 6)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return items