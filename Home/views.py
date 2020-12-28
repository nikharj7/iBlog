from django.shortcuts import render, HttpResponse, redirect
from Home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from MYBLOG.models import Post


# HTML Pages
def home(request):
    
    allPosts = Post.objects.all().order_by("-timeStamp")[0:3]
    context = {'allPosts' : allPosts}
    return render(request, 'home.html', context)

# def about(request):
#     return render(request, 'about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Message : please fill the form correctly !")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been sent! Thank you for contacting us.....")
        
    return render(request, 'contact.html')



def search(request):
    query = request.GET['query']
    if len(query)>80:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)

    if allPosts.count() == 0:
        messages.warning(request, "No search results. Please refine your query.")
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'search.html', params)


# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for erroeneous inputs
        # username should be under 10 charcters
        if len(username) >10:
            messages.error(request, "Username is too long.")
            return redirect('home')
        # Username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers.")
            return redirect('home')
        # Password should match
        if pass1 != pass2:
            messages.error(request, "Password doesn't match.")
            return redirect('home')

        
        # Create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your MyBlog account has been successfully created.")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')

        else:
            messages.error(request, "Invalid Credentials, Please try again ")
            return redirect('home')

    return HttpResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
    return HttpResponse('handleLogout')

 
    


    
  


