from django.contrib.auth.models import User
from django.db import models

from team.models import Team


class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    org_name = models.CharField(max_length=225, default='unknown')
    email = models.EmailField()
    address = models.CharField(max_length=255, default='unknown')
    description = models.TextField(blank=True, null=True)
    monthly_order = models.IntegerField(default=0)
    total_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer_type = models.CharField(max_length=20, choices=(('restaurant', 'Restaurant'), ('store', 'Store')), default='unknown')
    created_by = models.ForeignKey(User, related_name='clients', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    sales_rep = models.ForeignKey(User, related_name='clients_rep', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Calculate the total_order_value based on monthly_order
        self.total_order_value = self.monthly_order * 29.95
        super(Client, self).save(*args, **kwargs)

class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='client_comments', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='client_comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

class ClientFile(models.Model):
    team = models.ForeignKey(Team, related_name='client_files', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='clientfiles') #location of folder for uplaod
    created_by = models.ForeignKey(User, related_name='client_files', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

