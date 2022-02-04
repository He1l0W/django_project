from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from acc.models import User
from django.contrib import messages


# Create your views here.
def signup(request):
    if request.method =='POST':
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        ag = request.POST.get("uage")
        co = request.POST.get("ucom")
        pi = request.FILES.get("upic")
        User.objects.create_user(username=un,password=pw,age=ag, comment=co, pic=pi) 
        return redirect("acc:login")
    return render(request, "acc/signup.html")

def profile(requset):
    return render(requset, 'acc/profile.html')

def delete(request):
    if check_password(request.POST.get('passcheck'), request.user.password):
        request.user.pic.delete()
        request.user.delete()    
    return redirect('acc:index')

def update(request):
    if request.method =='POST':
        u = request.user
        pw = request.POST.get("upass")
        co = request.POST.get("ucom")
        pi = request.FILES.get("upic")
        if pw:
            u.set_password(pw)
        if pi:
            u.pic.delete
            u.pic = pi
        u.comment = co
        u.save()
        login(request, u)
        return redirect('acc:profile')
    return render(request, 'acc/update.html')

def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request, f'{user}님 환영합니다.')
            return redirect("acc:index")
        else: # 로그인 실패했어요~~ (19일차에 작성예정)
            messages.error(request, '아이디나 패스워드가 잘못됐습니다.')
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect("acc:index")