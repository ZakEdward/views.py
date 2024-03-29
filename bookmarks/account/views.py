from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditorForm, ProfileEditorForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action

def user_login(request):
    if request.method == 'POST':
        ### Создаём экземпляр формы с переданными данными
        form = LoginForm(request.POST)
        ### Форма валидируется
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'account/dashboard.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

@login_required
def dashboard(request):
    # По умолчанию показывать все действия
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # Показывает только на кого подписан
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')[:10].prefetch_related('target')[:10]
    # select_related - Один-ко-многим, prefetch_related - Многие-ко-многим !!! Всегда с аргументами
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


def edit(request):
    if request.method == 'POST':
        user_form = UserEditorForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditorForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '
                             'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditorForm(instance=request.user)
        profile_form = ProfileEditorForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html',
                  {'section': 'people',
                   'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html',
                  {'section': 'people',
                   'user': user})

@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_form=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_form=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error1'})
    return JsonResponse({'status': 'error2'})
