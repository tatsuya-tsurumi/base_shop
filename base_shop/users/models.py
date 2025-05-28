from django.db import models
from django.contrib.auth.models import(
BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy

class UserManager(BaseUserManager):
  def create_user(self, username, email, password):
    if not email:
      raise ValueError('Emailを入力してください')
    if not password:
      raise ValueError('Passwordを入力してください')
    user = self.model(
    username=username,
    email=self.normalize_email(email)
    )
    user.set_password(password)
    user.save()
    return user
  
  def create_superuser(self, username, email, password=None):
    user = self.create_user(
      username=username,
      email=email,
      password=password,
    )
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField('名前' ,max_length=150)
  email = models.EmailField('メールアドレス' ,max_length=255, unique=True)
  address = models.CharField('住所' ,max_length=255, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']
  
  objects = UserManager()
  
  def get_absolute_url(self):
    return reverse_lazy('users:home')