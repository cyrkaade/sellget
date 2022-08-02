from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class myUser(AbstractUser):
    
    # User model
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    SELLER = "SELLER"
    BUYER = "BUYER"
    TIER_CHOICES = (
        (SELLER, "Seller"),
        (BUYER, "Buyer"),
    )
    tier = models.CharField(max_length=20,
                  choices=TIER_CHOICES,
                  default="Buyer")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    name= models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Room(models.Model):
    # Rooms of lots' model.
    # Shade choices

    MAROON = "MAROON"
    YELLOW = "YELLOW"
    RED = 'RED'
    CHARTREUSE = 'CHARTREUSE'
    DARK_CYANIDE = 'DARK_CYANIDE'
    DECEPTIVE_BLUE = 'DECEPTIVE_BLUE'
    OCHRE = 'OCHRE'
    DARK_ORCHID = 'DARK_ORCHID'
    PINK_BROWN = 'PINK_BROWN'

    SHADE_CHOICES = (
        (MAROON, "Maroon"),
        (YELLOW, "Yellow"),
        (RED, "Red"),
        (CHARTREUSE, "Chartreuse"),
        (DARK_CYANIDE, "Dark Cyanide"),
        (DECEPTIVE_BLUE, "Deceptive Blue"),
        (OCHRE, "Ochre"),
        (DARK_ORCHID, "Dark Orchid"),
        (PINK_BROWN, "Pink-brown"),
    )
    YES = "YES"
    NO = "NO"
    BOOL_CHOICES = (
        (YES, "Yes"),
        (NO, "No"),
    )

    host = models.ForeignKey(myUser, on_delete=models.SET_NULL, null=True)
    flower_type = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    shade = models.CharField(max_length=200, choices=SHADE_CHOICES, default='Red')
    stock_quantity = models.PositiveIntegerField(default = 1, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    show_or_no = models.CharField(max_length=200, choices=BOOL_CHOICES, default='Yes')
    participants = models.ManyToManyField(myUser, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.flower_type)
        
    class Meta:
        ordering = ['-updated', '-created']

# Model of buying lots.
class Buy(models.Model):
    seller = models.CharField(max_length = 128, null = True, default='Anonymous')
    quantity = models.PositiveIntegerField(null=False, blank=True, default=1, validators=[MinValueValidator(1),])
    quantity_after = models.PositiveIntegerField(null=True, blank=True)
    buyers = models.TextField(null = True, default='')
    pricing = models.PositiveIntegerField(null = True)
    room_revenue = models.PositiveIntegerField(default = 0)
        

# Model of messaging (reviews)
class Message(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]