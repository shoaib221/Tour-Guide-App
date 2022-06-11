import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAdmin.settings")
django.setup()


class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(label='Your email')
    comment = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # Get 'initial' argument if any
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
            # We have initial arguments, fetch 'user' placeholder variable if any
            user = initial_arguments.get('user', None)
            # Now update the form's initial values if user
            if user:
                updated_initial['name'] = getattr(user, 'first_name', None)
                updated_initial['email'] = getattr(user, 'email', None)
            # You can also initialize form fields with hardcoded values
            # or perform complex DB logic here to then perform initialization
        updated_initial['comment'] = 'Please provide a comment'
        # Finally update the kwargs initial reference
        kwargs.update(initial=updated_initial)
        print(type(kwargs))
        super(ContactForm, self).__init__(*args, **kwargs)


ContactForm()
