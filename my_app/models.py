from django.db import models


class personal_information(models.Model):
    id= models.AutoField(primary_key=True)

    age = models.IntegerField()
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    children = models.IntegerField()
    smoker = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    charges = models.FloatField()
    telephone_no = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
         return '{}'.format(self.age)

    class Meta:
        verbose_name_plural = 'personal_information'

# Create your models here.
class appointment(models.Model):
    id=models.AutoField(primary_key=True)
    amka= models.IntegerField()
    bmi = models.FloatField()
    dose = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
         return '{}'.format(self.bmi)

    class Meta:
        verbose_name_plural = 'appointments'


