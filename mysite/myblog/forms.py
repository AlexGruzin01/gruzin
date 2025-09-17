from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class ContactForm(forms.Form):
    name = forms.CharField(label='', max_length=80, widget=forms.TextInput(attrs={'id': 'form-name', 'placeholder': 'Ф.И.О'}))
    email = forms.EmailField(label='', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    subject = forms.CharField(label='', max_length=80, widget=forms.TextInput(attrs={'placeholder': 'Тема'}))
    content = forms.CharField(label='Text', required=True, widget=forms.Textarea(attrs={'class': 'form-social-body__textarea','placeholder': 'Сообщение'}))


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Поисковый запрос',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите запрос...',
            'class': 'form-control'
        })
    )

    SEARCH_IN_CHOICES = [
        ('title', 'В заголовках'),
        ('content', 'В содержании'),
        ('both', 'Везде'),
    ]

    search_in = forms.ChoiceField(
        choices=SEARCH_IN_CHOICES,
        initial='both',
        widget=forms.RadioSelect,
        required=False
    )

    DATE_CHOICES = [
        ('all', 'За все время'),
        ('today', 'Сегодня'),
        ('week', 'За неделю'),
        ('month', 'За месяц'),
    ]

    date_range = forms.ChoiceField(
        choices=DATE_CHOICES,
        initial='all',
        widget=forms.RadioSelect,
        required=False
    )