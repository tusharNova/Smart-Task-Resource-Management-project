from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    display_name = models.CharField(max_length=120 , blank=True)
    avatar = models.ImageField(upload_to="avator/" , null=True,blank=True)

    def __str__(self):
        return self.display_name or self.get_full_name() or self.username()
    


class Project(models.Model):
    name = models.CharField(max_length=225)
    descriptions = models.TextField(blank=True)
    owner = models.ForeignKey(User , on_delete=models.CASCADE ,related_name='owned_project')
    member = models.ManyToManyField(User ,related_name="project" ,blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo' , 'to-do'),
        ('in_progress' , 'In Progress'),
        ('done' , 'Done'),
    ]

    PRIORITY_CHOICES =[
        (1 , 'Low'),(2 , 'Median'),(3 , 'High'),
    ]

    project = models.ForeignKey(Project , on_delete=models.CASCADE , related_name='task')
    title = models.CharField(max_length=225)
    descriptions = models.TextField(blank=True)
    assignee = models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank=True ,related_name="tasks")
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES , default='todo')
    priority =models.IntegerField(choices=PRIORITY_CHOICES , default=2)
    due_date = models.DateField(null=True ,blank=True )
    watchers = models.ManyToManyField(User , related_name='watching_task' , blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return f"{self.title} ({self.project.name})"
    

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
    

class Attachment(models.Model):
    task = models.ForeignKey(Task,  on_delete=models.CASCADE , related_name='attachments')
    file = models.FileField( upload_to='attachments/', max_length=100)
    update = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.task}"
    