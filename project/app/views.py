from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Contact,Friendspost
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'home/index.html')

def handleSignup(request):
    if(request.method == 'POST'):
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if len(username)>10:
            messages.warning(request,'username should be less than 10 characters')
            return redirect('/')
        if not username.isalnum():
            messages.warning(request,'username should contain only letters and numbers')
            return redirect('/')
        if pass1!=pass2:
            messages.warning(request,'password is incorrect')
            return redirect('/')
        try:
            if User.objects.get(username=username):
                messages.warning(request,'Username already taken')
                return redirect('/')
        except Exception as identifier:
            pass    
        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,'Signup successful Please Login')
        return redirect('/')

        

    return render(request,'home/index.html')

def handlelogin(request):
    if(request.method == 'POST'):
        loginusername=request.POST['username']
        loginpassword=request.POST['pass1']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.info(request,'Login Success')
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('/')

            
    
    
    return render(request,'home/index.html')

def handlelogout(request):
    logout(request)
    return render(request,'home/index.html')

def addpost(request):
    if (request.method=="POST"):
        title=request.POST.get('title')
        desc=request.POST.get('desc')
        name=request.POST.get('name')
        file=request.FILES['file']
        query=Friendspost(title=title,content=desc,img=file,author=name)
        query.save()
        messages.success(request,'Your Post has been Saved')
        return redirect('/friendsPost')

    return render(request,'home/addpost.html')

def blogPost(request):
    return render(request,'home/blogPost.html')

def friendsPost(request):
    if not request.user.is_authenticated:
        messages.warning(request,'Please Login and Try again')
        return redirect('/')
    posts=Friendspost.objects.all()
    context={'posts':posts}

    return render(request,'home/friendsPost.html',context)

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if (request.method=="POST"):
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('num')
        desc=request.POST.get('desc')
        from_email=settings.EMAIL_HOST_USER
        # print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        # your mail starts here
        connection=mail.get_connection()
        connection.open()
        #email1=mail.EmailMessage(name,desc,from_email,['kumar.153@iitj.ac.in'],connection=connection)
        email_admin=mail.EmailMessage(f'Email From {name}',f'Description :{desc} \n Email Address : {email} \n Phone : {phone}',from_email,['kumar.153@iitj.ac.in'],connection=connection)
        email_client=mail.EmailMessage('HARSHblog','Thanks for contacting us we will get back to you soon \n Thank You',from_email,[email],connection=connection)
        connection.send_messages([email_admin,email_client])
        connection.close()
        messages.warning(request,f'Thanks for Contacting Us {name}')
        return redirect('/contact')

    return render(request,'home/contact.html')