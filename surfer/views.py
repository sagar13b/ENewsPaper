from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from editor.models import NewsPost
from .models import NewsComment, NewsLike, CommentComment, FollowEditor, Notification, ReportComment
from account.models import User, EditorProfile
from .top_news import get_news
# Create your views here.
def homepage(request):
    if request.method == 'POST':
        d = request.POST['dat']
        return redirect('sdat', d)
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    nl = NewsPost.objects.filter(pub_status=True)
    nnl = []
    for n in nl:
        if n.ppub_day == d:
            nnl.append(n)
    catnl = {}
    for n in nnl:
        if n.category not in catnl:
            catnl[n.category] = [n]
        else:
            catnl[n.category].append(n)
    data = zip(catnl.keys(),catnl.values())
    return render(request, 'surfer/home.html', {'data':data,'d':d,'tn':get_news()})

def detail_news(request, nid):
    n = NewsPost.objects.get(id=nid)
    n.view_no += 1
    n.save()
    ncl = NewsComment.objects.filter(news_detail=n)
    #ncl = [nc1,nc2,..]
    data = []
    for nc in ncl:
        ccl = CommentComment.objects.filter(comment_detail=nc)
        data.append((nc, ccl))
        #data = [(nc1,[cc1,cc2,...]),(nc2,[cc1,cc2,..]),...]
    try:
        nl = NewsLike.objects.get(surfer_detail=request.user,news_detail=n)
    except:
        con = False
    else:
        con = True
    return render(request, 'surfer/news_detail.html',{'n':n,'data':data,'con':con})

@login_required(login_url='sin')
def comment_news(request, nid):
    n = NewsPost.objects.get(id=nid)
    nc = NewsComment()
    nc.surfer_detail = request.user
    nc.news_detail = n
    nc.comment = request.POST['c']
    nc.save()
    return redirect('sndetail', nid)

@login_required(login_url='sin')
def like_news(request, nid):
    n = NewsPost.objects.get(id=nid)
    try:
        nl = NewsLike.objects.get(surfer_detail=request.user,news_detail=n)
    except:
        nl = NewsLike()
        nl.news_detail = n
        nl.surfer_detail = request.user
        nl.save()
        n.like_no += 1
        n.save()
    else:
        nl.delete()
        n.like_no -= 1
        n.save()
    finally:
        return redirect('sndetail', nid)

@login_required(login_url='sin')
def comment_comment(request, cid):
    nc = NewsComment.objects.get(id=cid)
    cc = CommentComment()
    cc.surfer_detail = request.user
    cc.comment_detail = nc
    cc.comment = request.POST['cc']
    cc.save()
    return redirect('sndetail', nc.news_detail.id)

def category_news(request, cat):
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    nl = NewsPost.objects.filter(pub_status=True, category=cat)
    nnl = []
    for n in nl:
        if n.ppub_day == d:
            nnl.append(n)
    return render(request, 'surfer/category_news.html', {'nl': nnl, 'd': d, 'cat':cat})

def date_by_news(request, date):
    nl = NewsPost.objects.filter(pub_status=True)
    nnl = []
    for n in nl:
        if n.ppub_day == date:
            nnl.append(n)
    catnl = {}
    for n in nnl:
        if n.category not in catnl:
            catnl[n.category] = [n]
        else:
            catnl[n.category].append(n)
    data = zip(catnl.keys(),catnl.values())
    return render(request, 'surfer/date_news.html', {'data':data,'d':date})

def date_category_news(request, date, cat):
    nl = NewsPost.objects.filter(pub_status=True,category=cat)
    nnl = []
    for n in nl:
        if n.ppub_day == date:
            nnl.append(n)
    return render(request, 'surfer/category_date_news.html', {'nl':nnl,'cat':cat,'d':date})

def editor_profile(request, eid):
    e = User.objects.get(id=eid)
    ep = EditorProfile.objects.get(user_detail=e)
    el = FollowEditor.all_editor(request.user)
    if e in el:
        con = False
    else:
        con = True
    return render(request, 'surfer/editor_profile.html',{'e':e,'ep':ep,'con':con})

def follow_editor(request, eid):
    e = User.objects.get(id=eid)
    ep = EditorProfile.objects.get(user_detail=e)
    el = FollowEditor.all_editor(request.user)
    if e in el:
        FollowEditor.remove_editor(request.user, e)
        ep.no_followers -= 1
    else:
        ep.no_followers += 1
        FollowEditor.add_editor(request.user,e)
    ep.save()
    return redirect('seprofile', eid)

def subscribtion(request):
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    el = FollowEditor.all_editor(request.user)
    nl = []
    for e in el:
        enl = NewsPost.objects.filter(editor_detail=e,pub_status=True)
        for n in enl:
            if d == n.ppub_day:
                nl.append(n)
    return render(request, 'surfer/subscribtion.html',{'nl':nl,'el':el,'d':d})

def subscribtion_editor(request, eid):
    e = User.objects.get(id=eid)
    el = FollowEditor.all_editor(request.user)
    nl = NewsPost.objects.filter(editor_detail=e,pub_status=True).order_by('ppub_date')
    return render(request, 'surfer/subscribtion.html',{'nl':nl,'el':el})

def search_news(request):
    if request.method == 'POST':
        d = request.POST['d']
        nl = NewsPost.objects.filter(title__icontains=d)
        el = User.objects.filter(editor=True,admin=False)
        return render(request, 'surfer/search.html',{'d':d,'nl':nl,'l':len(nl),'el':el})

def advance_search_news(request):
    if request.method == 'POST':
        el = User.objects.filter(editor=True,admin=False)
        nl = NewsPost.objects.filter(title__icontains=request.POST['t'],pub_status=True)
        if request.POST['dat'] != '':
            nnl = []
            for n in nl:
                if n.ppub_day == request.POST['dat']:
                    nnl.append(n)
            nl = nnl
        if request.POST['edi'] != 'None':
            nnl = []
            e = User.objects.get(id=request.POST['edi'])
            for n in nl:
                if n.editor_detail == e:
                    nnl.append(n)
            nl = nnl
        if request.POST['cat'] != 'All':
            nnl = []
            for n in nl:
                if n.category == request.POST['cat']:
                    nnl.append(n)
            nl = nnl
        return render(request, 'surfer/search.html',{'nl':nl,'d':request.POST['t'],'el':el})

def show_notification(request):
    nl = Notification.list_notification(request.user)
    return render(request, 'surfer/notification.html',{'nl':nl})

def report_comment(request, cid, val):
    rc = ReportComment()
    rc.surfer_detail = request.user
    if val == 'nc':
        nc = NewsComment.objects.get(id=cid)
        rc.ncom = nc
        nid = nc.news_detail.id
    elif val == 'cc':
        rc.status = False
        cc = CommentComment.objects.get(id=cid)
        rc.ccom = cc
        nid = cc.comment_detail.news_detail.id
    rc.save()
    return redirect('sndetail',nid)

from .forms import NewsForm
def example(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.editor_detail = request.user
            form.save()
    else:
        return render(request, 'example.html',{'form':form})