from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def register(request):
    if request.method == "POST":
        # get the data from the user
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name') 
        username   = request.POST.get('username')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        email      = request.POST.get('email')

        # Check if password1 == password2
        if password1 == password2:
            if User.objects.filter(username=username).exists(): # chec for username in DB
                messages.info(request, 'Username is already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email is already Exists')
                return redirect('register')
            else:
                # Create new user 
                user = User.objects.create_user(first_name=first_name,last_name=last_name, username=username,password=password1, email=email)
                # save user to the database
                user.save()
                # check
                messages.success(request, f'Welcome {username}, you have successfully Created an account')
                return redirect('login') # redirect to the home page
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html', {})

# Handle the login from here
def login(request):
    # Check for the POST
    if request.method == 'POST':
        # Get the data from the user
        username   = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        # Check if the user exist or not
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else: 
            messages.info(request, 'Enter the correct username and password')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

# The most beautiful logout function in the world 
def logout(request):
    auth.logout(request)
    messages.success(request, "You Logged out")
    return redirect('/')