from django.shortcuts import render, redirect
from django.utils import timezone
from book.models import Book

# Create your views here.
def index(request):
    b = request.user.book_set.all().order_by('-pubdate')
    context = {
        'blist' : b,
    }
    return render(request, 'book/index.html', context)

def create(request):
    if request.method == 'POST':
        im = request.POST.get('impo')
        sn = request.POST.get('sname')
        li = request.POST.get('link')
        con = request.POST.get('con')
        print(im,sn,li,con)
        if sn and li and con:

            if im:
                im = True
            else:
                im = False
            Book(site_name=sn, site_url=li, content=con, user=request.user, impo=im, pubdate=timezone.now()).save()
            return redirect('book:index')
    return render(request, 'book/create.html')