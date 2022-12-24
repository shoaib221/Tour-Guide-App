from django import forms
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
        kwargs.update(initial=updated_initial)  # ********
        # print('********', type(initial=updated_initial))
        print(type(kwargs))  # <class 'dict'>
        for k1 in kwargs:
            print(k1, kwargs.get(k1, None))
            # initial {'name': 'shoaib', 'email': 'a@b.com', 'comment': 'Please provide a comment'}

        super(ContactForm, self).__init__(*args, **kwargs)


class User:
    first_name = 'shoaib'
    email = 'a@b.com'


u = User()
ContactForm(initial={'user': u})

'''
output
<class 'dict'>
initial {'name': 'shoaib', 'email': 'a@b.com', 'comment': 'Please provide a comment'}
'''

print('sec1')


def pass_kwargs(**kwargs):
    print(kwargs)  # {'initial': {'one': 1, 'two': 2}}
    print(type(kwargs))  # <class 'dict'>
    updated_initial = {'two': 3}

    # if1
    '''
    kwargs.update(initial=updated_initial)
    print(kwargs)  # {'initial': {'two': 3}, 'kappa': {'three': 3}}
    '''

    # if2
    '''
    kwargs['initial'].update(updated_initial)
    print(kwargs)  # {'initial': {'one': 1, 'two': 3}, 'kappa': {'three': 3}}
    '''


pass_kwargs(initial={'one': 1, 'two': 2}, kappa={'three': 3})

# Always use the initial argument or __init__ method to populate forms with initialization data and keep them unbound *

# validators


def validate_comment_word_count(value):
      count = len(value.split())
      if count < 30:
            raise forms.ValidationError(('Please provide at least a 30 word message,
	    % (count)s words is not descriptive enough'), params={'count': count},)


class ContactForm(forms.Form):
      name = forms.CharField(required=False)
      email = forms.EmailField(label='Your email')
      comment = forms.CharField(widget=forms.Textarea, validators=[
                                validate_comment_word_count])





'''
link = https://www.webforefront.com/django/formprocessing.html
