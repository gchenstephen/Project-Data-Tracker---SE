from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(Iteration)
admin.site.register(Defect)
admin.site.register(Timer)
admin.site.register(Developer)
admin.site.register(Phase)
