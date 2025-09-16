from django.contrib import admin
from .models import User , Comment , Attachment , Task , Project

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Task)
admin.site.register(Project)
