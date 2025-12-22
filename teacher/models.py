from django.db import models
from django.contrib.auth.models import User
from nur_comp.models import ListTeacher, ListStudent, Group

# 1. Мугалимдин журналы (Упайлар жана катышуу)
class Journal(models.Model):
    # Тандоо варианттары
    TYPE_CHOICES = [
        ('presence', 'Келди (+2 балл)'),
        ('good_job', 'Жакшы тапшырма (+3 балл)'),
        ('absence', 'Келген жок (-2 балл)'),
    ]

    teacher = models.ForeignKey(ListTeacher, on_delete=models.CASCADE, verbose_name="Мугалим")
    student = models.ForeignKey(ListStudent, on_delete=models.CASCADE, verbose_name="Окуучу")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    entry_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Түрү")
    points = models.IntegerField(default=0, verbose_name="Балл")

    def save(self, *args, **kwargs):
        # Сиз айткан логика боюнча баллдарды автоматтык түрдө эсептөө
        if self.entry_type == 'presence':
            self.points = 2
        elif self.entry_type == 'good_job':
            self.points = 3
        elif self.entry_type == 'absence':
            self.points = -2
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Журнал жазуусу"
        verbose_name_plural = "Журнал"

# 2. Сабактардын графиги
class Schedule(models.Model):
    DAYS = [
        (1, 'Дүйшөмбү'), (2, 'Шейшемби'), (3, 'Шаршемби'),
        (4, 'Бейшемби'), (5, 'Жума'), (6, 'Ишемби'), (7, 'Жекшемби'),
    ]

    teacher = models.ForeignKey(ListTeacher, on_delete=models.CASCADE, verbose_name="Мугалим")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    day_of_week = models.IntegerField(choices=DAYS, verbose_name="Апта күнү")
    start_time = models.TimeField(verbose_name="Башталышы")
    end_time = models.TimeField(verbose_name="Аякташы")
    room = models.CharField(max_length=50, blank=True, verbose_name="Кабинет")

    class Meta:
        verbose_name = "График"
        verbose_name_plural = "Графиктер"

# 3. Үй тапшырмалары (Placeholder катары)
class Homework(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Тема")
    description = models.TextField(verbose_name="Тапшырма")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Үй тапшырма"
        verbose_name_plural = "Үй тапшырмалар"