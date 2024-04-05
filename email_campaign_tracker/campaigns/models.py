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
class Email(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(Subscriber,related_name='emails')

# Email Recipient Class
class EmailRecipient(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'{self.email} - {self.subscriber}'



