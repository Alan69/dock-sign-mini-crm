from django.db import models
from django.contrib.auth.models import User

class PersonalSkill(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProfessionalSkill(models.Model):
    name = models.CharField(max_length=255)
    percent = models.IntegerField()

    def __str__(self):
        return self.name

class Education(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    mob_number = models.CharField(max_length=12, blank=True, null=True)
    personal_skill = models.ManyToManyField(PersonalSkill, blank=True)
    professional_skill = models.ManyToManyField(ProfessionalSkill, blank=True)
    education = models.ManyToManyField(Education, blank=True)
    experience = models.IntegerField(blank=True, null=True)



    def __str__(self):
        return self.user.username