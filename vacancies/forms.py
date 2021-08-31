from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from vacancies.models import *


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ApplicationForm(forms.ModelForm):
    written_cover_letter = forms.CharField(label='Сопроводительное письмо', widget=forms.Textarea(attrs={'rows': 8,
                                                                                                         'class': 'form-control'}))
    written_username = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    written_phone = forms.CharField(label='Ваш телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class ResumeForm(forms.ModelForm):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    work_status = forms.ModelChoiceField(queryset=WorkStatus.objects.all(), label='Готовность к работе',
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    salary = forms.IntegerField(label='Желаемый оклад', widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), label='Специализация',
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    qualification = forms.ModelChoiceField(queryset=Qualification.objects.all(), label='Квалификация',
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    education = forms.CharField(label='Образование', widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))
    experience = forms.CharField(label='Опыт работы', widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))
    link = forms.URLField(label='Ссылка', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'http://anylink.github.io'}))

    class Meta:
        model = Resume
        fields = ['name', 'surname', 'work_status', 'salary', 'specialty', 'qualification', 'education', 'experience',
                  'link']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='Месторасположение', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    employee_count = forms.IntegerField(label='Колличество сотрудников',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(label='Логотип', widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']


class VacanciesEditForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), initial=0, label='Специализация',
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    skills = forms.CharField(label='Требуемые навыки', widget=forms.Textarea(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))
    salary_min = forms.IntegerField(label='Зарплата от', widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary_max = forms.IntegerField(label='Зарплата до', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']


class VacanciesCreateForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), label='Специализация',
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    skills = forms.CharField(label='Требуемые навыки', widget=forms.Textarea(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))
    salary_min = forms.IntegerField(label='Зарплата от', widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary_max = forms.IntegerField(label='Зарплата до', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

