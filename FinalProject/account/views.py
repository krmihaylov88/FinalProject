import ast
import copy
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.urls import reverse_lazy

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, AccountData
from ..cart.cart import Cart


# class SignInView(auth_views.LoginView):
#     template_name = 'account/login.html'

def user_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(request,
                            username=cd['username'],
                            password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # [print(f'{el} => {val}') for el,val in request.session.items()]
                record = AccountData.objects.get(username=cd['username'])
                if record:
                    res = ast.literal_eval(record.value)
                    request.session['cart'] = res
                return redirect('dashboard')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)


# class SignOutView(auth_views.LogoutView):
#     next_page = reverse_lazy('shop')

def user_logout(request):
    # [print(f'{el} => {val}') for el,val in request.session.items()]
    username = request.user.username
    key = [key for key in request.session.keys() if key == 'cart']
    value = request.session.get('cart')
    try:
        record = AccountData.objects.get(username=username, key=key)
        record.value = value
        record.save()
    except AccountData.DoesNotExist:
        record = AccountData(username=username, key=key, value=value)
        record.save()
    logout(request)
    return redirect('shop:product_list')


@login_required
def index(request):
    context = {
        'section': 'dashboard',
    }
    return render(request, 'account/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            key = [key for key in request.session.keys() if key == 'cart']
            value = request.session.get('cart')
            record = AccountData(username=request.POST['username'], key=key, value=value)
            record.save()
            context = {
                'new_user': new_user,
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()

    context = {
        'user_form': user_form,
    }
    return render(request, 'account/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit.html', context)
