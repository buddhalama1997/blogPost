from django.db import models
from matplotlib.pyplot import title

# create a table for blogPost with title and description as field name
class blogPost(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()