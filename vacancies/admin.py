from django.contrib import admin
from .models import Company, Vacancy, Specialty, Application, Qualification, WorkStatus, Resume


admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Specialty)
admin.site.register(Application)
admin.site.register(Qualification)
admin.site.register(WorkStatus)
admin.site.register(Resume)
