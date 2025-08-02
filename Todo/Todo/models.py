from django.db import models
from django.contrib.auth.models import User

class todo(models.Model):
    # Django automatically adds an 'id' field as the primary key.
    # We can omit the 'sno' field for simplicity.
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the Todo object.
        This is helpful for Django's admin interface and debugging.
        """
        return self.title