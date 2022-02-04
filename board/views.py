from email import message
from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(requset):
    pg = requset.GET.get('page', 1)
    cate = requset.GET.get('cate', '')
    kw = requset.GET.get('kw', '')

    if kw:
        if cate == 'sub':
            b = Board.objects.filter(subject__startswith=kw)
        elif  cate == 'wri':
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        else:
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()

    
    pag = Paginator(b, 10)
    obj = pag.get_page(pg)
    context = {
        'blist' : obj,
        'cate' : cate,
        'kw' : kw,
    }
    return render(requset, 'board/index.html', context)

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        'b' : b,
        'rlist' : r,
    }
    return render(request, 'board/detail.html', context)

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete
    else:
        messages.error(request, "아이디나 패스워드가 다릅니다.")
    return redirect('board:index')

def create(request):
    if request.method == 'POST':
        sub = request.POST.get('sub')
        con = request.POST.get('con')
        Board(subject=sub, writer=request.user, content=con, pubdate=timezone.now()).save()

        return redirect('board:index')
    return render(request, 'board/create.html')

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get('comment')
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    return redirect('board:detail', bpk)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else: # 19일차 에러메세지 띄울 예정!
        messages.error(request, "잘못된 접근입니다.")
    return redirect("board:detail", bpk)


def update(request, bpk):
    b = Board.objects.get(id=bpk)
    # 다른 사람이 악의적으로 접근했을 때 (19일차 추가)
    # 또 다른 방법 코드의 부하 계산
    # if request.user != b.writer:
    #     return redirect('board:index')
    # if request.method == 'POST':
    #         b.subject = request.POST.get('sub')
    #         b.content = request.POST.get('con')
    #         b.save()
    #         return redirect('board:detail', bpk)
    
    if b.writer == request.user:
        if request.method == 'POST':
            b.subject = request.POST.get('sub')
            b.content = request.POST.get('con')
            b.save()
            return redirect('board:detail', bpk)
    else:
        return redirect('board:index')
    context = {
        'b' : b,
    }
    return render(request, 'board/update.html', context)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likely.add(request.user)
    return redirect('board:detail', bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likely.remove(request.user)
    return redirect('board:detail', bpk)
