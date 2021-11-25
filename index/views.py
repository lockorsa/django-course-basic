from django.views.generic import TemplateView

from adminapp.views.mixins import CallableMixin


class Index(CallableMixin, TemplateView):
    template_name = 'index/index.html'


class Contact(CallableMixin, TemplateView):
    template_name = 'index/contact.html'


# алиасы
index = Index.as_view()
contact = Contact.as_view()
