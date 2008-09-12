from django import forms
from django.contrib.auth.models import User

RESERVED_USERNAMES = """
admin administrator root webmaster postmaster test testuser testclient staff
""".split()
USERNAME_CHARS_FIRST = 'abcdefghijklmnopqrstuvwxyz'
USERNAME_CHARS = USERNAME_CHARS_FIRST + '0123456789_.-'
USERNAME_MIN_LENGTH = 2
PASSWORD_MIN_LENGTH = 6


class UserCreateForm(forms.Form):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)
    repeat = forms.CharField(max_length=40, widget=forms.PasswordInput)
    email = forms.EmailField()

    class Media:
        js = ("/static/js/jquery.js",
              "/static/js/jquery.form.js")

    def clean_first_name(self):
        """
        Check that the first name starts with an uppercase letter.
        """
        first_name = self.cleaned_data['first_name']
        if not first_name:
            return ''
        if not first_name[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            raise forms.ValidationError(
                "Name should start with a capital letter.")
        if len(first_name) > 4 and first_name.upper() == first_name:
            raise forms.ValidationError(
                "Name should not be all uppercase.")
        return first_name

    def clean_last_name(self):
        """
        Check that the last name starts with an uppercase letter.
        """
        last_name = self.cleaned_data['last_name']
        if not last_name:
            return ''
        if not last_name[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            raise forms.ValidationError(
                "Name should start with a capital letter.")
        if len(last_name) > 4 and last_name.upper() == last_name:
            raise forms.ValidationError(
                "Name should not be all uppercase.")
        return last_name

    def clean_username(self):
        """
        Check that the username is sensible and available.
        """
        username = self.cleaned_data['username'].strip()
        if len(username) < USERNAME_MIN_LENGTH:
            raise forms.ValidationError(
                "The username must have at least %d characters." %
                USERNAME_MIN_LENGTH)
        if username[0] not in USERNAME_CHARS_FIRST:
            raise forms.ValidationError(
                "Username must start with a lowercase letter.")
        for index in range(len(username)):
            if username[index] not in USERNAME_CHARS:
                raise forms.ValidationError(
                    "Username may contain only simple letters (a-z0-9_.-).")
        if username in RESERVED_USERNAMES:
            raise forms.ValidationError("This username is reserved.")
        print 'validating username'
        if User.objects.filter(username=username).count():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        """
        Check that the password is long enough and not too silly.
        """
        password = self.cleaned_data['password']
        if len(password) < PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(
                "The password must have at least %d characters." %
                PASSWORD_MIN_LENGTH)
        if password.isdigit() or password == len(password) * password[0]:
            raise forms.ValidationError("The password is too simple.")
        return password

    def clean_repeat(self):
        """
        Check that the password and repeat is the same.
        """
        if 'password' not in self.cleaned_data:
            return
        password = self.cleaned_data['password']
        repeat = self.cleaned_data['repeat']
        if repeat != password:
            raise forms.ValidationError("Enter the same password again.")
        return repeat
