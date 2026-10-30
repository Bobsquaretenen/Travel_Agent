from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, BookingRequest

# Классы из вашего CSS для полей
INPUT_ATTRS = {'class': 'form__input'}
CHECKBOX_ATTRS = {'class': 'form__checkbox'}


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Минимум 3 символа'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={**INPUT_ATTRS, 'placeholder': 'you@example.com'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': '+7 (___) ___-__-__'}))

    # ДОБАВЛЯЕМ min_length=8 И minlength="8"
    password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            **INPUT_ATTRS,
            'placeholder': 'Минимум 8 символов',
            'minlength': '8'
        }),
        error_messages={
            'min_length': 'Пароль должен содержать минимум 8 символов.'
        }
    )

    # ДОБАВЛЯЕМ min_length=8 И minlength="8"
    password2 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            **INPUT_ATTRS,
            'placeholder': 'Повторите пароль',
            'minlength': '8'
        }),
        error_messages={
            'min_length': 'Пароль должен содержать минимум 8 символов.'
        }
    )

    pd_consent = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs=CHECKBOX_ATTRS))
    terms = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs=CHECKBOX_ATTRS))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone')


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={**INPUT_ATTRS, 'placeholder': 'you@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={**INPUT_ATTRS, 'placeholder': 'Пароль'}))


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        # Убрали 'subject' из списка
        fields = ('name', 'email', 'phone', 'message')
        widgets = {
            'name': forms.TextInput(attrs=INPUT_ATTRS),
            'email': forms.EmailInput(attrs=INPUT_ATTRS),
            'phone': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': '+7 (___) ___-__-__'}),
            # Убрали 'subject' из widgets
            'message': forms.Textarea(attrs={**INPUT_ATTRS, 'rows': 5, 'placeholder': 'Напишите, что вы думаете о нашем сервисе...'}),
        }

    privacy = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs=CHECKBOX_ATTRS))


class CardForm(forms.Form):
    number = forms.CharField(
        max_length=19,
        min_length=16,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': '0000 0000 0000 0000'})
    )
    expiry = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'ММ/ГГ'})
    )
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': 'CVV'})
    )

    pd_consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form__checkbox'}),
        error_messages={'required': 'Необходимо ваше согласие на обработку персональных данных.'}
    )

    def clean_number(self):
        number = self.cleaned_data['number'].replace(' ', '')
        if not number.isdigit():
            raise forms.ValidationError("Номер карты должен содержать только цифры.")
        return number