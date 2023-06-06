from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self,name, email, e_email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    e_email = self.normalize_email(e_email)
    user = self.model(
        name = name,
        email=email,
        e_email=e_email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password,name='',e_email='', **extra_fields):
    return self._create_user(name,email,e_email, password, False, False, **extra_fields)

  def create_superuser(self, email, password,name='',e_email='', **extra_fields):
    user=self._create_user(name,email,e_email, password, True, True, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    e_email = models.EmailField(max_length=254, unique=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _

# from .managers import CustomUserManager
 
    
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(_("username"), max_length=30, unique=True)
#     email = models.EmailField(_("email address"), unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email
    
    
# CREATE TABLE IF NOT EXISTS "users_customuser" (
#   "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#   "password" varchar(128) NOT NULL,
#   "last_login" datetime NULL,
#   "is_superuser" bool  NULL,
#   "first_name" varchar(150)  NULL,
#   "last_name" varchar(150)  NULL,
#   "is_staff" bool  NULL,
#   "is_active" bool  NULL,
#   "date_joined" datetime  NULL,
#   "email" varchar(254) NOT NULL UNIQUE,
#   "e_email" varchar(254) NULL UNIQUE
# );

 
# CustomUser = get_user_model()

# class CustomLogEntry(LogEntry):
#     user_custom = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     class Meta:
#         proxy = True
        
# class User(AbstractUser):
#     groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_set',
#         blank=True,
#         help_text=_('Specific permissions for this user.'),
#         verbose_name=_('user permissions'),
#     )
#     e_email = models.EmailField(_('emergency email'), unique=True, blank=True, null=True)
    
#     objects = CustomUserManager()

# CustomUserTe = get_user_model()

# class CustomLogEntry(LogEntry):
#     user = models.ForeignKey(CustomUserTe, on_delete=models.CASCADE)

#     class Meta:
#         proxy = True

class Video(models.Model):
    name = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = basename(self.video_file.name)
        super().save(*args, **kwargs)

    video_file = models.FileField(upload_to='videos/')