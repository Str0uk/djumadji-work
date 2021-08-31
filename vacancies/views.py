import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView, UpdateView
from django.views.generic import CreateView

from . import models
from .models import Specialty, Company, Vacancy, Application, Resume
from .forms import RegisterForm, LoginForm, ApplicationForm, ResumeForm, ProfileForm, CompanyForm, VacanciesEditForm, VacanciesCreateForm
from .utils import DataMixin

specialties = Specialty.objects.all()
title_specialties = []
for i in specialties:
    title_specialties.append(i.title)
companies = Company.objects.all()
vacancies = Vacancy.objects.all()


class MainView(TemplateView):
    def get(self, request, *args, **kwargs):
        if  request.user.is_authenticated:
            resume_len = len(Resume.objects.filter(user=request.user))
            resume = Resume.objects.filter(user=request.user).first()
            mycompany_len = len(Company.objects.filter(owner=request.user))
            mycompany = Company.objects.filter(owner=request.user).first()
        else:
            resume = ''
            resume_len = 0
            mycompany_len = 0
            mycompany = ''
        return render(request, 'week3/index.html', {'specialties': specialties, 'title_specialties': title_specialties,
                                                    'companies': companies[:8], 'resume_len': resume_len,
                                                    'resume': resume, 'mycompany_len': mycompany_len,
                                                    'mycompany': mycompany, 'vacancies': vacancies})


class VacanciesViews(DataMixin, CreateView):
    form_class = ApplicationForm
    template_name = 'week3/vacancy.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_company'] = Vacancy.objects.filter(id=self.kwargs['pk']).first()
        context['pk'] = self.kwargs['pk']
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.vacancy = Vacancy.objects.filter(id=self.kwargs['pk']).first()
        instance.save()
        return redirect('application_send', self.kwargs['pk'])


    # def get(self, request, pk, *args, **kwargs):
    #     data_company = Vacancy.objects.filter(id=pk)
    #     form = ApplicationForm
    #     if request.user.is_authenticated:
    #         resume_len = len(Resume.objects.filter(user=request.user))
    #         resume = Resume.objects.filter(user=request.user).first()
    #         mycompany_len = len(Company.objects.filter(owner=request.user))
    #         mycompany = Company.objects.filter(owner=request.user).first()
    #     else:
    #         resume = ''
    #         resume_len = 0
    #         mycompany_len = 0
    #         mycompany = ''
    #     return render(request, 'week3/vacancy.html', {'data_company': data_company[0], 'pk': pk, 'form': form,
    #                                                   'resume_len': resume_len, 'resume': resume,
    #                                                   'mycompany_len': mycompany_len, 'mycompany': mycompany})


class AllVacanciesView(DataMixin, ListView):
    model = Vacancy
    template_name = 'week3/all_vacancies.html'
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = len(Vacancy.objects.all())
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class GenreVacanciesView(DataMixin, ListView):
    model = Vacancy
    template_name = 'week3/vacancies_genre.html'
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = len(Vacancy.objects.filter(specialty__code=self.kwargs['genre']))
        context['genre'] = self.kwargs['genre']
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Vacancy.objects.filter(specialty__code=self.kwargs['genre'])


class CompanyVacanciesView(DataMixin, ListView):
    model = Vacancy
    template_name = 'week3/vacancies_company.html'
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = len(Vacancy.objects.filter(company__name=self.kwargs['company']))
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Vacancy.objects.filter(company__name=self.kwargs['company'])


class SpecializationView(TemplateView):
    def get(self, request, company, genre, *args, **kwargs):
        company_specialization = Company.objects.filter(name=company)
        specialty_specializations = Specialty.objects.filter(code=genre)
        vacancies = Vacancy.objects.filter(company=company_specialization[0]).filter(
            specialty=specialty_specializations[0])
        if request.user.is_authenticated:
            resume_len = len(Resume.objects.filter(user=request.user))
            resume = Resume.objects.filter(user=request.user).first()
            mycompany_len = len(Company.objects.filter(owner=request.user))
            mycompany = Company.objects.filter(owner=request.user).first()
        else:
            resume = ''
            resume_len = 0
            mycompany_len = 0
            mycompany = ''
        return render(request, 'week3/vacancies.html', {'vacancies': list(vacancies),
                                                        'genre': specialty_specializations[0].title, 'company': company,
                                                        'count': len(vacancies), 'resume_len': resume_len,
                                                        'resume': resume, 'mycompany_len': mycompany_len,
                                                        'mycompany': mycompany})


class CompanyView(TemplateView):
    def get(self, request, id, *args, **kwargs):
        company_vacancies = Company.objects.filter(id=id)
        vacancies_of_company = Vacancy.objects.filter(company=company_vacancies[0])
        if  request.user.is_authenticated:
            resume_len = len(Resume.objects.filter(user=request.user))
            resume = Resume.objects.filter(user=request.user).first()
            mycompany_len = len(Company.objects.filter(owner=request.user))
            mycompany = Company.objects.filter(owner=request.user).first()
        else:
            resume = ''
            resume_len = 0
            mycompany_len = 0
            mycompany = ''
        return render(request, 'week3/company.html', {'company_vacancies': company_vacancies[0],
                                                      'vacancies_of_company': vacancies_of_company,
                                                      'count_vacancies': len(vacancies_of_company),
                                                      'resume_len': resume_len, 'resume': resume,
                                                      'mycompany_len': mycompany_len, 'mycompany': mycompany})


# class VacanciesSendView(CreateView):
#     template_name = 'week4/sent.html'
#     model = Application
#     fields = ['written_username', 'written_phone', 'written_cover_letter']

class VacanciesSendView(DataMixin, CreateView):
    model = Application
    template_name = 'week4/sent.html'
    fields = ['written_username', 'written_phone', 'written_cover_letter', 'user']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect('main')


class MyCompanyView(TemplateView):
    def get(self, request, *args, **kwargs):
        if  request.user.is_authenticated:
            resume_len = len(Resume.objects.filter(user=request.user))
            resume = Resume.objects.filter(user=request.user).first()
            mycompany_len = len(Company.objects.filter(owner=request.user))
            mycompany = Company.objects.filter(owner=request.user).first()
        else:
            resume = ''
            resume_len = 0
            mycompany_len = 0
            mycompany = ''
        return render(request, 'week3/no_company.html', {'resume_len': resume_len, 'resume': resume,
                                                        'mycompany_len': mycompany_len, 'mycompany': mycompany})


class MyCompanyCreate(DataMixin, CreateView):
    form_class = CompanyForm
    template_name = 'week3/company_create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return redirect('main')


class MyCompanyEditView(DataMixin, UpdateView):
    model = Company
    template_name = 'week3/company-edit.html'
    form_class = CompanyForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class MyVacanciesView(DataMixin, ListView):
    model = Vacancy
    template_name = 'week4/vacancy-list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(company__owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class MyVacanciesEditView(DataMixin, UpdateView):
    model = Vacancy
    template_name = 'week4/vacancy-edit.html'
    form_class = VacanciesEditForm
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(vacancy__id=self.kwargs['pk'])
        context['count_applications'] = len(Application.objects.filter(vacancy__id=self.kwargs['pk']))
        context['pk'] = self.kwargs['pk']
        context['allowed_vacancy'] = Vacancy.objects.filter(company__owner=self.request.user)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'week4/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'week4/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class NoResumeView(TemplateView):
    def get(self, request, *args, **kwargs):
        if  request.user.is_authenticated:
            resume_len = len(Resume.objects.filter(user=request.user))
            resume = Resume.objects.filter(user=request.user).first()
            mycompany_len = len(Company.objects.filter(owner=request.user))
            mycompany = Company.objects.filter(owner=request.user).first()
        else:
            resume = ''
            resume_len = 0
            mycompany_len = 0
            mycompany = ''
        return render(request, 'week4/no-resume.html', {'resume_len': resume_len, 'resume': resume,
                                                        'mycompany_len': mycompany_len, 'mycompany': mycompany})


class ResumeEditView(DataMixin, UpdateView):
    model = Resume
    template_name = 'week4/resume-edit.html'
    form_class = ResumeForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class ResumeCreateView(DataMixin, CreateView):
    form_class = ResumeForm
    template_name = 'week4/create_resume.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect('main')


class ProfileView(DataMixin, UpdateView):
    model = User
    template_name = 'week4/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class MyVacanciesCreate(DataMixin, CreateView):
    model = Vacancy
    template_name = 'week4/vacancy_create.html'
    form_class = VacanciesCreateForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.company = Company.objects.filter(owner=self.request.user).first()
        instance.published_at = datetime.date.today()
        print(instance)
        instance.save()
        return redirect('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class Search(DataMixin, ListView):
    template_name = 'week4/search.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login')
