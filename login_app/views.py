from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.http import HttpResponseRedirect

# Create your views here.
def signup_view(request):
    # POSTかチェック
    if request.method == 'POST':
        # フォームオブジェクトを作成
        form = SignupForm(request.POST)
        # 入力した要件を満たしているかチェック
        if form.is_valid():
            user = form.save()
            # アカウント登録後に自動的にログイン
            login(request, user) 
            # ログインページにリダイレクト
            return redirect(reverse_lazy('login'))
    else:
        # 空のフォームを作成
        form = SignupForm()
    
    # フォームを送信していないとき新規登録ページを表示    
    param = {
        'form': form
    }
    return render(request, 'login_app/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        # ユーザーの入力したデータをフォームに結びつける(バインド)
        form = LoginForm(request, data=request.POST)
        # フォームが有効かチェック
        if form.is_valid():
            user = form.get_user()
            
            if user:
                login(request, user)
                # 'next' パラメータからリダイレクト先を取得
                next_page = request.GET.get('next', reverse_lazy('list'))
                # リダイレクト先を指定してリダイレクト
                return redirect(next_page)
                
    else:
        form = LoginForm()

    param = {
        'form': form,
    }

    return render(request, 'login_app/login.html', param)

from django.urls import reverse
from django.shortcuts import redirect

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        # ログイン画面にリダイレクトするために、ログイン画面のURLを解決する
        login_url = reverse('login')
        return HttpResponseRedirect(login_url)
    elif request.method == 'GET':
        return render(request, 'login_app/logout_confirm.html')
    return JsonResponse({'error': 'Only GET and POST methods are allowed'})

def logout_view(request):
    logout(request)
    
    return render(request, 'login_app/logout.html')
