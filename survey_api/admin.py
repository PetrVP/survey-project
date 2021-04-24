from django.contrib import admin
from .models import Survey, Questions, UserAnswer

admin.site.register(Survey)
admin.site.register(Questions)
admin.site.register(UserAnswer)