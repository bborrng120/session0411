from django.db import models

class TodoItem(models.Model):
    title = models.CharField(max_length=100)  
    description = models.TextField(blank=True)  

    def __str__(self):
        return self.title
