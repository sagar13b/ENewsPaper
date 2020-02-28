from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_editor(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.editor = True
        user.active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.editor = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=20, null=True)
    lname = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='UserEmail',unique=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname','lname']
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    editor = models.BooleanField(default=False)
    surfer = models.BooleanField(default=True)
    objects = UserManager()

    @property
    def is_active(self):
        return self.active

    @property
    def is_editor(self):
        return self.editor

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_surfer(self):
        return self.surfer

    def has_perm(self, perms, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def fullname(self):
        if self.mname != None:
            fn = self.fname + ' ' + self.mname + ' ' + self.lname
            return fn
        else:
            fn = self.fname + ' ' + self.lname
            return fn

class EditorProfile(models.Model):
    user_detail = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
    profile_pic = models.ImageField(upload_to='editor/',null=True)
    address = models.CharField(max_length=50)
    no_followers = models.IntegerField(default=0)