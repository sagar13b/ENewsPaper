from django.db import models
from account.models import User
from editor.models import NewsPost

# Create your models here.
class NewsComment(models.Model):
    surfer_detail = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    news_detail = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

class NewsLike(models.Model):
    surfer_detail = models.ForeignKey(User, on_delete=models.CASCADE)
    news_detail = models.ForeignKey(NewsPost, on_delete=models.CASCADE)

class CommentComment(models.Model):
    surfer_detail = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_detail = models.ForeignKey(NewsComment, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

class FollowEditor(models.Model):
    surfer_detail = models.ForeignKey(User, on_delete=models.CASCADE)
    editor_list = models.ManyToManyField(User, related_name='Editor')

    @classmethod
    def add_editor(cls, s, e):
        fe, status = cls.objects.get_or_create(surfer_detail=s)
        fe.editor_list.add(e)
        fe.save()
        return fe

    @classmethod
    def remove_editor(cls, s, e):
        fe = cls.objects.get(surfer_detail=s)
        fe.editor_list.remove(e)
        fe.save()
        return fe

    @classmethod
    def all_editor(cls, s):
        fe, status = cls.objects.get_or_create(surfer_detail=s)
        el = fe.editor_list.all()
        return el

class Notification(models.Model):
    surfer_detail = models.ForeignKey(User, on_delete=models.CASCADE)
    news_list = models.ManyToManyField(NewsPost)

    @classmethod
    def add_notification(cls, s, n):
        nm, status = cls.objects.get_or_create(surfer_detail=s)
        nm.news_list.add(n)
        nm.save()
        return nm

    @classmethod
    def list_notification(cls, s):
        nm, status = cls.objects.get_or_create(surfer_detail=s)
        nl = nm.news_list.all()
        return nl

class ReportComment(models.Model):
    status = models.BooleanField(default=True)
    ncom = models.ForeignKey(NewsComment, on_delete=models.CASCADE, null=True)
    ccom = models.ForeignKey(CommentComment, on_delete=models.CASCADE, null=True)
    surfer_detail = models.ForeignKey(User, on_delete=models.CASCADE)