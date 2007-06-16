from django import newforms as forms
from shotserver04.websites import extract_domain
from shotserver04.websites.models import Domain, Website


class UrlForm(forms.Form):
    """
    URL input form.
    """
    url = forms.URLField(
        max_length=400,
        label=_("Enter your web address here:"))

    def cleaned_dict(self):
        """
        Get or create domain and website.
        """
        url = self.cleaned_data['url']
        if url.count('/') == 2:
            url += '/' # Slash after domain name
        domain, created = Domain.objects.get_or_create(
            name=extract_domain(url, remove_www=True))
        website, created = Website.objects.get_or_create(
            url=url, domain=domain)
        return {'website': website}
