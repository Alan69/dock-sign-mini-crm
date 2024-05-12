from django.contrib import admin
from .models import Profile, PersonalSkill, ProfessionalSkill, Education
# Register your models here.

admin.site.register(Profile)
admin.site.register(PersonalSkill)
admin.site.register(ProfessionalSkill)
admin.site.register(Education)