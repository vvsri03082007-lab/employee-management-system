from django.db import models

class Employee(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    designation = models.CharField(max_length=100)

    salary = models.IntegerField()

    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class DeletedEmployee(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    designation = models.CharField(max_length=100)

    salary = models.IntegerField()

    phone = models.CharField(max_length=15)

    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name