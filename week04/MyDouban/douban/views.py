from django.shortcuts import render

# Create your views here.
from . models import T1


def books_short(request):
    # 从models取数据传给template
    queryset = T1.objects.all()
    condtions = {'n_star__gt': 3}
    shorts = queryset.filter(**condtions).order_by('n_star')

    return render(request, 'index.html', locals())
