from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.utils.translation import ugettext_lazy as _

class Client(models.Model):
    '''
    Customer/client model.
    '''

    #Fields
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    email = models.CharField(max_length=120, null=True)

    #Relationships
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

class Portfolio(models.Model):
    '''
    Investment porfolio model. Has a many to one relationship with its parent, Client.

    '''
    
    #Fields
    portfolio_name = models.CharField(max_length=120)

    #Relationships
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    #Attributes
    ytd = models.FloatField(default=0)
    sharpe = models.FloatField(default=0)
    sortino = models.FloatField(default=0)
    valatrisk = models.FloatField(default=0)
    top3 = models.CharField(max_length=25, default='')
    total_val = models.FloatField(default=0)
    year_beg_val = models.FloatField(default=0)

    def __str__(self):
        return self.portfolio_name

class Security(models.Model):
    '''
    Investable security model. Has a many to one relationship with its parent, Portfolio.
    '''
    
    #Fields
    SECURITIES = (
        ('Equity', 'Equity'),
        ('Bond', 'Bond'),
        ('Crypto', 'Crypto')
    )
    security_type = models.CharField(max_length=120, choices=SECURITIES)
    ticker = models.CharField(max_length=12)  
    amount = models.FloatField()

    #Relationships
    portfolio_parent = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker


#Tried the following code to make the email a user's username/unique identifier

"""

class UserManager(BaseUserManager):
    '''
    Define a model manager for User model with no username field.
    '''

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''
        Create and save a User with the given email and password.
        '''
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        '''
        Create and save a regular User with the given email and password.
        '''
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        '''
        Create and save a SuperUser with the given email and password.
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    '''
    User model
    '''

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
"""
