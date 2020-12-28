from django.shortcuts import render, HttpResponse, redirect
from MYBLOG.models import Post, BlogComment
from django.contrib import messages
from MYBLOG.templatetags import extras



def blogHome(request):
    allPosts = Post.objects.all().order_by("-timeStamp")
    context = {'allPosts' : allPosts}
    messages.success(request, "Your can submit your posts through contact us form.")
    return render(request, 'BlogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    # views = request.session.get('views',0)
    # request.session['views'] = views + 1
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)

    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments, 'user': request.user,  'replyDict': replyDict}
    return render(request, 'BlogPost.html', context)

def postComment(request):
    if request.method =="POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno) 
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")
