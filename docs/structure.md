# Structure
The architecture is fairly easy and simplified. It's a monolith without any API or anything special aside from a little client reactivity provided by Alpine.js.

## Table of Contents




## Apps
The project is divided in 4 apps, which in reality is only 2:
- `ledger`: This app is the one that handles the **transactions** and the products.
- `accounts`: This app is the one that handles the **users** and the authentication.
- `theme`: This app is the one that handles the **Tailwind** integration. *Don't worry about it.*

There are as well 3 other folder:
- `config`: Where all the configuration and settings files are.
- `static`: Where all the static files are.
- `templates`: Where all the templates are. This is the only folder that has **HTML** files.
- `locale`: Where all the translations are that are not in the database objects. ChatGPT works fine for most of the words ;).

## Templates
The templates are the only files that have **HTML** in them. They are the ones that are rendered by the server and sent to the client. They are the ones that have the **Alpine.js** code in them.

Alpine.js is a library which sends a really little bundle to the client, and it's the one that handles the reactivity of the client. It's really easy to use and it's really powerful. It is mainly used in the **buy.html** for the search feature and the tags filtering.

## Forms
The forms are the ones that handle the data that is sent to the server. They are the ones that have the **Django** code in them. Most of the logic of how to handle the data is in the forms.

Let's see a little bit how it works:
```python
class ProfileDeleteForm(forms.Form):
    """
    Form for deleting user profile.
    """
    password = forms.CharField(max_length=100, required=True, label=_("Password"), widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileDeleteForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise ValidationError(_("Wrong password."))
        return password

    def save(self, commit=True):
        self.user.delete()
        return self.user
```

The `__init__` method is handled by when the form is created in the view. It's the one that handles the `user` parameter. The `clean_password` method is the one that handles the validation of the password (**checks** the data). And the `save` method is the one that handles the deletion of the user (**execute** the action).

This is a really simple example, but it's the same for all the forms. The only difference is that some forms have more fields and more logic.

## Views
The views are the ones that handle the data that is sent to the client. They are the ones that have the **Django** code in them. Most of the logic of how to handle the data is in the views.

Let's see a little bit how it works:
```python
class ProfileDeleteView(FormView):
    """
    View for deleting user profile.
    """
    template_name = 'registration/profile_delete.html'
    form_class = ProfileDeleteForm
    success_url = reverse_lazy('accounts:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save(self.request.user)
        messages.success(self.request, 'Your account has been deleted!')
        return super().form_valid(form)
```

The `template_name` is the one that handles the template that is going to be rendered. The `form_class` is the one that handles the form that is going to be used. The `success_url` is the one that handles the URL that is going to be redirected when the form is valid.

The `get_form_kwargs` method is the one that handles the `user` parameter. The `form_valid` method is the one that handles the deletion of the user (**execute** the action) and the message that is going to be shown to the user.

This is a really simple example, but it's the same for all the views. The only difference is that some views have more fields and more logic.

## Models
The models are the ones that handle the data that is stored in the database. They are the ones that have the **Django** code in them. Most of the logic of how to handle the data is in the models. It's fairly easy. If any questions, ask ChatGPT, but it should be easy to understand.

It is worth noticing that there is a **CustomUser** in accounts which it's an extension of the normal User to add the **balance**.

In the ledger, the **products** have tags for classifying them. This is why there is a ProductTag and TaggedProduct model. The first one is the one that handles the tags and the second one is the one that handles the relation between the products and the tags.

Continuing in the ledger, the **Transaction** is an abstract model which Purchase, Ingress, TransferSend and TransferReceive inherit from. The first one is the one that handles the purchases, the second one is the one that handles the ingresses from mobilepay, the third one is the one that handles the transfers sent and the fourth one is the one that handles the transfers received. TransferSend is the one who creates TransferReceive (for admin). The reason why they are separated is because they have different fields and different logic.

## Translation
The translation is handled by **Django-modeltranslation**. It used for translating inside the database. It's really easy to use and it's really powerful. It is mainly used in the **products** and **transactions** and **tags** models.

## Middleware
The middleware in accounts is only to redirect the user to /login/ in case it isn't authenticated. It's really simple and it's only 1 file.