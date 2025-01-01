from django import forms
from .models import MailingUnit, MailReceiver

class MailingUnitForm(forms.ModelForm):
    receivers = forms.ModelMultipleChoiceField(
        queryset=MailReceiver.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        label="Получатели"
    )

    class Meta:
        model = MailingUnit
        fields = ['message', 'receivers']

    def __init__(self, *args, **kwargs):
        super(MailingUnitForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control'})