from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm
from .forms import LoginForm
from django.contrib import messages 

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}')
#             return redirect('homepage')
#     else:
#         form = UserRegisterForm()

#     return render(request, 'users/register.html', {'form': form})


@login_required
def account(request):
    return render(request, 'users/account.html')



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.success(request, "You're logged in")
            return redirect('account')
    else:
        messages.error(request, "Incorrect username or passsword, please try again.")

    return render(request, 'users/login.html')
    # return render(request, 'users/login.html', {'form': form})



def logout(request):
    return render(request, 'users/logout.html')


def show_messages(request):
    return render(request, 'pages/messages.html')