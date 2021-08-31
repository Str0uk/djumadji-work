from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from data import jobs, companies, specialties
from freelance.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.CharField(max_length=128)
    employee_count = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def delete(self, *args, **kwargs):
        # для удаления нам нужен объект стораджа, где хранится файл с аватаркой и его путь
        self.picture.storage.delete(self.picture.path)
        super(Specialty, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=128)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies', blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')
    skills = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    salary_min = models.CharField(max_length=32)
    salary_max = models.CharField(max_length=32)
    published_at = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=128)
    written_phone = models.CharField(max_length=16)
    written_cover_letter = models.TextField(blank=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vacancy')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application')


class WorkStatus(models.Model):
    status = models.CharField(max_length=127, db_index=True)

    def __str__(self):
        return self.status


class Qualification(models.Model):
    quality = models.CharField(max_length=127)

    def __str__(self):
        return self.quality


class Resume(models.Model):
    name = models.CharField(max_length=127)
    surname = models.CharField(max_length=127)
    work_status = models.ForeignKey(WorkStatus, on_delete=models.CASCADE, related_name='work_status')
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='specialty')
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE, related_name='qualification')
    education = models.CharField(max_length=255)
    experience = models.CharField(max_length=511)
    link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True)


'''
migrat = []
for company in companies:
    migrat.append(Company(name=company["title"], location=company["location"],
                          description=company["description"],
                          employee_count=company["employee_count"],
                          id=company["id"]))
    migrat[-1].save()

migrat_specialty = []
for specialty in specialties:
    migrat_specialty.append(Specialty(title=specialty["title"],
                                      code=specialty["code"]))
    migrat_specialty[-1].save()


migrat_job = []
for job in jobs:
    migrat_job.append(Vacancy(title=job["title"], specialty = migrat_specialty[1],
                              company=migrat[job["company"]-1], skills=job["skills"], description=job["description"],
                              salary_min=job["salary_from"], salary_max=job["salary_to"], published_at=job["posted"]))
    migrat_job[-1].save()
'''