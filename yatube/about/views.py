from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """The class returns a page about the site author."""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """The class returns a page about the site's technologies."""
    template_name = 'about/tech.html'
