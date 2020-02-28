from django.db import models
from account.models import User
# Create your models here.
class NewsPost(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    body = models.TextField()
    image = models.ImageField(upload_to='news/', null=True)
    img_source = models.CharField(max_length=50, null=True)
    epub_date = models.DateTimeField(auto_now_add=True)
    ppub_date = models.DateTimeField(auto_now_add=False,null=True)
    category = models.CharField(max_length=20)
    pub_status = models.BooleanField(default=False)
    editor_detail = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    like_no = models.IntegerField(default=0)
    view_no = models.IntegerField(default=0)

    @property
    def epub_day(self):
        return self.epub_date.strftime('%Y-%m-%d')

    @property
    def ppub_day(self):
        if self.ppub_date is not None:
            return self.ppub_date.strftime('%Y-%m-%d')