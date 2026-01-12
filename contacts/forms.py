from django import forms
from django.contrib.auth import get_user_model

from .models import Contact

User = get_user_model()


class ContactRequestForm(forms.Form):
    to_user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label='Пользователь',
        widget=forms.Select(attrs={
            'class': 'form-input'
        })
    )

    def __init__(self, *args, **kwargs):
        self.from_user = kwargs.pop('from_user', None)  # ← безопасно
        if self.from_user is None:
            raise ValueError("ContactRequestForm требует аргумент from_user")
        super().__init__(*args, **kwargs)

        # исключаем себя
        queryset = User.objects.exclude(id=self.from_user.id)

        # исключаем уже существующие связи
        existing = Contact.objects.filter(
            from_user=self.from_user
        ).values_list('to_user_id', flat=True)

        self.fields['to_user'].queryset = queryset.exclude(id__in=existing)

    def clean_to_user(self):
        to_user = self.cleaned_data['to_user']

        if Contact.objects.filter(
            from_user=self.from_user,
            to_user=to_user
        ).exists():
            raise forms.ValidationError('Заявка уже отправлена')

        return to_user
