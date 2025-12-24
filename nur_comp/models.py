from django.db import models
from django.contrib.auth.models import User



GENDER_CHOICES = (
    ('M', 'Эркек (Мужской)'),
    ('F', 'Аял (Женский)'),
    ('O', 'Башка (Другой)'),
)

class Branch(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name

class ListTeacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fio = models.CharField(max_length=50)
    email = models.EmailField()
    birthday = models.DateField()
    address = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    def __str__(self):
        return self.fio

class Group(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(ListTeacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class ListStudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    birthday = models.DateField()
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.full_name

class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    def __str__(self):
        return self.name

class AnalyticsReport(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(null=True, blank=True)
    def __str__(self):
        return self.title

