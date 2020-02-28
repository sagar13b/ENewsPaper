from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, logout
from .models import NewsPost
from account.models import User, EditorProfile
# Create your views here.
def homepage(request):
    return render(request, 'editor/home.html')

def create_post(request):
    if request.method == 'POST':
        p = NewsPost()
        p.title = request.POST['title']
        p.body = request.POST['content']
        p.category = request.POST['category']
        p.editor_detail = request.user
        p.summary = request.POST['summary']
        p.epub_date = timezone.now()
        try:
            p.image = request.FILES['image']
            p.img_source = request.POST['image_src']
            p.save()
        except:
            p.save()
        return redirect('ehome')
    else:
        return render(request, 'editor/create_post.html')

def my_u_news(request):
    nl = NewsPost.objects.filter(editor_detail=request.user,pub_status=False)
    return render(request, 'editor/my_u_news.html',{'nl':nl})

def my_p_news(request):
    nl = NewsPost.objects.filter(editor_detail=request.user,pub_status=True)
    return render(request, 'editor/my_p_news.html',{'nl':nl})

def news_detail(request, nid):
    n = NewsPost.objects.get(id=nid)
    return render(request, 'editor/news_detail.html',{'n':n})

def update_detail(request, nid):
    n = NewsPost.objects.get(id=nid)
    if request.method == 'POST':
        n.title = request.POST['title']
        n.body = request.POST['content']
        n.category = request.POST['category']
        n.summary = request.POST['summary']
        try:
            n.image = request.FILES['image']
            n.img_source = request.POST['image_src']
            n.save()
        except:
            n.save()
        return redirect('endetail', n.id)
    else:
        return render(request, 'editor/update_news.html', {'n':n})

def delete_post(request, nid):
    n = NewsPost.objects.get(id=nid)
    n.delete()
    return redirect('unews')

def all_news(request,eid):
    el = User.objects.filter(editor=True,admin=False)
    if eid == 0:
        nl = NewsPost.objects.filter(editor_detail=el[0])
    else:
        e = User.objects.get(id=eid)
        nl = NewsPost.objects.filter(editor_detail=e)
    return render(request, 'editor/all_news.html', {'el':el,'nl':nl})

def view_profile(request):
    ep = EditorProfile.objects.get(user_detail=request.user)
    return render(request, 'editor/profile.html',{'ep':ep})

def update_profile(request):
    ep = EditorProfile.objects.get(user_detail=request.user)
    if request.method == 'POST':
        u = request.user
        u.fname = request.POST['fname']
        u.lname = request.POST['lname']
        if request.POST['mname'] is not None:
            u.mname = request.POST['mname']
        u.email = request.POST['email']
        u.save()
        ep.address = request.POST['address']
        ep.phone_no = request.POST['phone_no']
        try:
            ep.profile_pic = request.FILES['ppic']
            ep.save()
        except:
            ep.save()
        return redirect('eprofile')
    else:
        return render(request, 'editor/update_profile.html',{'ep':ep})

def change_password(request):
    if request.method == 'POST':
        u = authenticate(email=request.user.email,password=request.POST['pass'])
        if u is not None:
            if request.POST['pass1'] == request.POST['pass2']:
                logout(request)
                u.set_password(request.POST['pass1'])
                u.save()
                return redirect('sin')
            else:
                return render(request,'editor/change_password.html',{'error':'Password did not match'})
        else:
            return render(request, 'editor/change_password.html',{'error':'Password is incorrect'})
    else:
        return render(request, 'editor/change_password.html')