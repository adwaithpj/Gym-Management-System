from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout 
from .forms import GymAdminCreationForm,LoginForm,GoogleForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from .models import GymAdmin

def login_page(request):
    if request.user.is_authenticated:
        print("User is already authenticated")
        return redirect('authentication:complete_signup')
    
    if request.method == 'POST':
        form = LoginForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                
                remember_me = request.POST.get('remember_me')
                
                if remember_me:
                    request.session.set_expiry(604800)  # 1 week in seconds
                else:
                    request.session.set_expiry(86400)
                return redirect('authentication:complete_signup')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request,'auth/login.html',{'form':form})


def signup(request):
    if request.method == 'POST':
        form = GymAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            
            return redirect('authentication:login')
    else:
        form = GymAdminCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

def password_reset(request):
    pass


@login_required
def test(request):
    return render(request,'auth/test.html',{
        'user':request.user
    })




@login_required
def complete_signup(request):
    if request.user.phone_number:
        return redirect('home:dashboard')
    if request.method == 'POST':
        form = GoogleForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if not phone_number.isdigit() or len(phone_number) != 10:
                form.add_error('phone_number', 'Enter a valid 10-digit phone number.')
            else:
                # Update the logged-in user's phone number
                request.user.phone_number = phone_number
                request.user.save()
                messages.success(request, 'Your phone number has been updated.')
                return redirect('home:dashboard')  # Redirect to a success page or profile page

    else:
        form = GoogleForm()
    return render(request, 'auth/complete_signup.html', {'form': form})

@login_required
def logout_page(request):
    logout(request)
    return redirect('authentication:login')