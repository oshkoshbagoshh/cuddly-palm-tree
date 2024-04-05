from django.contrib import admin

# Register your models here.
from .models import Campaign, Subscriber, Email, EmailRecipient

admin.site.register(Campaign)
admin.site.register(Subscriber)
admin.site.register(Email)
admin.site.register(EmailRecipient)

