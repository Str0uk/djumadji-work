from vacancies.models import Resume, Company


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            context['resume_len'] = len(Resume.objects.filter(user=self.request.user))
            context['resume'] = Resume.objects.filter(user=self.request.user).first()
            context['user'] = self.request.user
            context['mycompany_len'] = len(Company.objects.filter(owner=self.request.user))
            context['mycompany'] = Company.objects.filter(owner=self.request.user).first()
        return context
