from django.shortcuts import render, redirect
from django.utils import timezone
from editor.models import NewsPost
from account.models import User, EditorProfile
from surfer.models import Notification, FollowEditor, NewsComment, NewsLike, CommentComment, ReportComment

# Create your views here.
def homepage(request):
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    el = User.objects.filter(editor=True,admin=False,active=True)
    data = []
    for e in el:
        nl = NewsPost.objects.filter(editor_detail=e,pub_status=True)
        nnl = []
        lcount = 0
        vcount = 0
        for n in nl:
            lcount += n.like_no
            vcount += n.view_no
            if n.ppub_day == d:
                nnl.append(n)
        pop = ((2*lcount)+vcount+1)/(len(nl)+1)
        data.append((e,len(nnl),pop))
    nl = NewsPost.objects.filter(pub_status=True).order_by('-view_no')
    nnl = []
    for n in nl:
        if n.ppub_day == d:
            nnl.append(n)
    return render(request, 'publisher/home.html',{'data':data,'nl':nnl,'anl':nl})

def unpublished_news(request):
    if request.method == 'POST':
        d = request.POST['dat']
        return redirect('aunpubdate', d)
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    nl = NewsPost.objects.filter(pub_status=False)
    nnl = []
    for n in nl:
        if n.epub_day == d:
            nnl.append(n)
    return render(request, 'publisher/unpublished.html',{'nl':nnl})

def unpublished_category_news(request, cat):
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    nl = NewsPost.objects.filter(pub_status=False, category=cat)
    nnl = []
    for n in nl:
        if n.epub_day == d:
            nnl.append(n)
    return render(request, 'publisher/unpublished.html',{'nl':nnl})

def unpublished_by_date(request, d):
    nl = NewsPost.objects.filter(pub_status=False)
    dnl = []
    for n in nl:
        if n.ppub_day == d:
            dnl.append(n)
    return render(request, 'publisher/unpublished_date.html',{'nl':dnl,'d':d})

def unpublished_by_date_category(request, d, cat):
    nl = NewsPost.objects.filter(pub_status=False, category=cat)
    nnl = []
    for n in nl:
        if d == n.epub_day:
            nnl.append(n)
    return render(request, 'publisher/unpublished_date.html',{'nl':nnl,'d':d})

def published_news(request):
    if request.method == 'POST':
        date = request.POST['dat']
        return redirect('apubdate', date)
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    nl = NewsPost.objects.filter(pub_status=True)
    nnl = []
    for n in nl:
        if d == n.ppub_day:
            nnl.append(n)
    return render(request, 'publisher/published.html',{'nl':nnl})

def published_category_news(request, cat):
    d = timezone.now()
    d = d.strftime('%Y-%m-%d')
    nl = NewsPost.objects.filter(pub_status=True, category=cat)
    nnl = []
    for n in nl:
        if n.epub_day == d:
            nnl.append(n)
    return render(request, 'publisher/published.html',{'nl':nnl})

def published_by_date(request, d):
    nl = NewsPost.objects.filter(pub_status=True)
    nnl = []
    for n in nl:
        if n.ppub_day == d:
            nnl.append(n)
    return render(request, 'publisher/published_date.html',{'nl':nnl,'d':d})

def published_by_date_category(request, d, cat):
    nl = NewsPost.objects.filter(pub_status=True, category=cat)
    nnl = []
    for n in nl:
        if n.ppub_day == d:
            nnl.append(n)
    return render(request, 'publisher/published_date.html',{'nl':nnl,'d':d})

def delete_news(request, nid):
    n = NewsPost.objects.get(id=nid)
    n.delete()
    return redirect('aunpub')

def publish_news(request, nid):
    n = NewsPost.objects.get(id=nid)
    n.pub_status = True
    n.ppub_date = timezone.now()
    n.save()
    fel = FollowEditor.objects.all()
    for fe in fel:
        el = fe.editor_list.all()
        for e in el:
            if e == n.editor_detail:
                Notification.add_notification(fe.surfer_detail,n)
    return redirect('aunpub')

def detail_news(request, nid):
    n = NewsPost.objects.get(id=nid)
    ncl = NewsComment.objects.filter(news_detail=n)
    data = []
    for nc in ncl:
        ccl = CommentComment.objects.filter(comment_detail=nc)
        data.append((nc,ccl))
    return render(request, 'publisher/detail_news.html',{'n':n,'data':data})

def editor_list(request):
    el = User.objects.filter(editor=True,admin=False)
    epl = []
    for e in el:
        ep = EditorProfile.objects.get(user_detail=e)
        epl.append(ep)
    data = zip(el,epl)
    return render(request, 'publisher/editor_list.html', {'data':data})

def editor_detail(request, eid):
    e = User.objects.get(id=eid)
    ep = EditorProfile.objects.get(user_detail=e)
    return render(request, 'publisher/editor_profile.html',{'e':e,'ep':ep})

def editor_remove(request, eid):
    e = User.objects.get(id=eid)
    e.delete()
    return redirect('aelist')

def editor_news(request, eid):
    e = User.objects.get(id=eid)
    nl = NewsPost.objects.filter(editor_detail=e)
    return render(request, 'publisher/editor_news.html', {'nl':nl,'e':e})

def search_news(request):
    if request.method == 'POST':
        s = request.POST['s']
        nl = NewsPost.objects.filter(title__icontains = s)
        return render(request, 'publisher/search.html',{'nl':nl})

def validate_editor(request, eid):
    e = User.objects.get(id=eid)
    if e.active:
        e.active = False
    else:
        e.active = True
    e.save()
    return redirect('aelist')

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
                return render(request,'publisher/change_password.html',{'error':'Password did not match'})
        else:
            return render(request, 'publisher/change_password.html',{'error':'Password is incorrect'})
    else:
        return render(request, 'publisher/change_password.html')

def list_report(request):
    rcl = ReportComment.objects.all()
    return render(request, 'publisher/report.html',{'rcl':rcl})

def delete_report(request, rid):
    rc = ReportComment.objects.get(id=rid)
    if rc.status:
        nc = rc.ncom
        nc.delete()
    else:
        cc = rc.ccom
        cc.delete()
    rc.delete()
    return redirect('areport')

def ignore_report(request, rid):
    rc = ReportComment.objects.get(id=rid)
    rc.delete()
    return redirect('areport')