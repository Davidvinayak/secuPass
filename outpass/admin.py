from django.contrib import admin
from .models import User,UserProfile, Student, Faculty, Parent,Outpass
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Parent)
admin.site.register(Outpass)