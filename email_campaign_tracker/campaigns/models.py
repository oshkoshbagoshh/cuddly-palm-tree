from django.db import models

# Create your models here.


# Campaign class
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name

# subscriber class
class Subscriber(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.email
    

# Email Class 

# Email Recipient Class

