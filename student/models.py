from django.db import models
from django.contrib.auth.models import User
# Башка колдонмолордогу моделдерди импорттоо
# nur_comp - сиздин негизги колдонмоңуздун аты болсо:
from nur_comp.models import Group, ListTeacher

class StudentProfile(models.Model):
    """ Окуучунун жеке маалыматтары """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fio = models.CharField(max_length=255, verbose_name="Аты-жөнү")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name="Группасы")
    phone = models.CharField(max_length=20, verbose_name="Телефон номери", blank=True)
    parents_phone = models.CharField(max_length=20, verbose_name="Ата-энесинин номери", blank=True)
    address = models.TextField(verbose_name="Дареги", blank=True)
    photo = models.ImageField(upload_to='students/', null=True, blank=True, verbose_name="Сүрөтү")

    class Meta:
        verbose_name = "Окуучу"
        verbose_name_plural = "Окуучулар"

    def __str__(self):
        return self.fio

class StudentGrade(models.Model):
    """ Окуучунун упайлары жана катышуусу """
    ENTRY_TYPES = (
        ('present', 'Келди'),
        ('absent', 'Жок'),
        ('late', 'Кечикти'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grades')
    teacher = models.ForeignKey(ListTeacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES, default='present')
    points = models.IntegerField(default=0, verbose_name="Упай / Баа")
    comment = models.CharField(max_length=255, blank=True, verbose_name="Мугалимдин пикири")

    class Meta:
        verbose_name = "Баалоо"
        verbose_name_plural = "Баалоо журналы"

    def __str__(self):
        return f"{self.student.fio} - {self.date} - {self.points}"