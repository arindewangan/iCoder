from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# HTML Pages

def home(request):
    allPosts = Post.objects.all()
    params = {'allPosts':allPosts}
    return render(request,'home/index.html',params)

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET.get('query')
    if len(query)>80:
        allPosts= Post.objects.none()
    else:
        matchTitle = Post.objects.filter(title__icontains=query)
        matchContent = Post.objects.filter(content__icontains=query)
        allPosts = matchTitle.union(matchContent)

    params = {'allPosts':allPosts,'query':query}
    return render(request,'blog/search.html',params)

# Authentication APIs

def handleSignup(request):
    if request.method=='POST':
        # Get the parameters
        username = request.POST['signupUsername']
        fname = request.POST['signupFName']
        lname = request.POST['signupLName']
        email = request.POST['signupEmail']
        password = request.POST['signupPassword']
        cnfpassword = request.POST['signupCnfPassword']

        # Check Inputs
        if len(username)>12:
            messages.error(request, " Your user name must be under 12 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers")
            return redirect('home')
        if (password!= cnfpassword):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myUser = User.objects.create_user(username,email,password)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()
        messages.success(request,'Your iCoder has been  successfully created.')
        return redirect('/')

    else:
        return HttpResponse('Error 404 - Not Found')

def handleLogin(request):
    if request.method=='POST':
        # Get the parameters
        loginuser = request.POST['loginUsername']
        loginpass = request.POST['loginPassword']
        user=authenticate(username=loginuser,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request, " User Logged in Successfully")
            return redirect('home')
        else:
            messages.error(request, " Invalid Credentials, Please try again")
            return redirect('home')
    else:
        return HttpResponse('Error 404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')