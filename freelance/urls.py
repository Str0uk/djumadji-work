from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from vacancies.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', AllVacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/<str:genre>', GenreVacanciesView.as_view(), name='vacancies_genre'),
    path('companies/<str:company>', CompanyVacanciesView.as_view(), name='vacancies_company'),
    path('vacancies/<str:company>/<str:genre>', SpecializationView.as_view()),
    path('vacancy/<int:pk>', VacanciesViews.as_view(), name='vacancy'),
    path('vacancy/<int:pk>/send', VacanciesSendView.as_view(), name='application_send'),
    path('companies/<int:id>', CompanyView.as_view()),
    path('resume/', NoResumeView.as_view(), name='no_resume'),
    path('resume/edit/<int:pk>', ResumeEditView.as_view(), name='resume_edit'),
    path('resume/create', ResumeCreateView.as_view(), name='create_resume'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/create', MyCompanyCreate.as_view(), name='mycompany_create'),
    path('mycompany/edit/<int:pk>', MyCompanyEditView.as_view(), name='mycompany_edit'),
    path('mycompany/vacancies', MyVacanciesView.as_view(), name='my_company_vacancies'),
    path('mycompany/vacancies/create', MyVacanciesCreate.as_view(), name='vacancies_create'),
    path('mycompany/vacancies/<int:pk>', MyVacanciesEditView.as_view(), name='vacancy_edit'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterView.as_view()),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('search/', Search.as_view(), name='search'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
