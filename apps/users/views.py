from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserProfileForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

# Create your views here.

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 验证用户类型是否匹配
            if user.user_type == user_type:
                login(request, user)
                messages.success(request, f'欢迎回来，{user.username}！')
                return redirect('home')
            else:
                messages.error(request, '用户类型不匹配，请选择正确的用户类型。')
        else:
            messages.error(request, '用户名或密码错误。')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('books:book_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息更新成功！')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
