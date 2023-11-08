from django.shortcuts import render, redirect
from .forms import CustomLoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            # Log in the user
            user = form.get_user()
            print(user)
            login(request, user)
            # Redirect to a success page, e.g., home page
            return redirect('home')
        else:
            print('invalid form')
            print(form.errors)
            return redirect('home')
    else:
    
        form = CustomLoginForm()
        context = {
            'form': form
        }
    return render(request, 'users/login.html',context)
# def signin(request):
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         form = CustomLoginForm(request, request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect('home')
#     else:
#         form = CustomLoginForm()

#     return render(request, 'users/login.html', {"form": form})

def signout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            return redirect('home')
        else:
            # messages.error(request, "Invalid user details")
            pass

    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {"form": form})