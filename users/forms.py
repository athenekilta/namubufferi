from django.forms import Form
from django.forms import fields


class ClaimBalanceForm(Form):
    name_in_namubuffa = fields.CharField()
    email = fields.EmailField()