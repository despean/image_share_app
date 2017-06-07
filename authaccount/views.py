from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact


def main_index(request):
  return render(request, 'account/index.html')


def user_login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)

    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(username=cd['username'],
                          password=cd['password'])
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponse('Authenticated ' \
                              'successfully')
        else:
          return HttpResponse('Disabled account')
      else:
        return HttpResponse('Invalid login')
  else:
    form = LoginForm()
  return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
  return render(request,
                'account/dashboard.html',
                {'section': 'dashboard'})


def register(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
      # Create a new user object but avoid saving it yet
      new_user = user_form.save(commit=False)
      # Set the chosen password
      new_user.set_password(
        user_form.cleaned_data['password'])
      # Save the User object
      new_user.save()
      profile = Profile.objects.create(user=new_user)
      return render(request,
                    'account/register_done.html',
                    {'new_user': new_user})
  else:
    user_form = UserRegistrationForm()
  return render(request,
                'account/register.html',
                {'user_form': user_form})


@login_required
def edit(request):
  if request.method == 'POST':
    user_form = UserEditForm(instance=request.user,
                             data=request.POST)
    profile_form = ProfileEditForm(
      instance=request.user.profile,
      data=request.POST,
      files=request.FILES)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Profile updated ' \
                                'successfully')
      return redirect('/account')
    else:
      messages.error(request, 'Error updating your profile')
  else:
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
  return render(request, 'account/edit.html',
                {'user_form': user_form,
                 'profile_form': profile_form})


from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@login_required
def user_list(request):
  users = User.objects.filter(is_active=True)
  return render(request,
                'account/user/list.html',
                {'section': 'people',
                 'users': users})


@login_required
def user_detail(request, username):
  user = get_object_or_404(User,
                           username=username,
                           is_active=True)
  return render(request,
                'account/user/detail.html',
                {'section': 'people',
                 'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
  user_id = request.POST.get('id')
  action = request.POST.get('action')
  if user_id and action:
    try:
      user = User.objects.get(id=user_id)
      if request.user != user:
        if action == 'follow':
          Contact.objects.get_or_create(user_from=request.user, user_to=user)
        else:
          Contact.objects.filter(user_from=request.user, user_to=user).delete()
        return JsonResponse({'status': 'ok'})
      else:
        messages.success(request, 'You can\'t follow your self')


    except User.DoesNotExist:
      return JsonResponse({'status': 'ko'})

  return JsonResponse({'status': 'ko'})