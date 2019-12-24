from django import forms
from questions.models import Question, Tag, Profile, Answer
from django.contrib.auth.models import User


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags'}))

    class Meta:
        model = Question
        fields = ['title', 'text']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your question'}),
        }

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.author = self.profile
        if commit:
            obj.save()

        tags = self.cleaned_data.get('tags')
        tags_list = [x.lower().strip() for x in tags.split(',') if x]

        for tag in tags_list:
            if Tag.objects.filter(name=tag).exists():
                t = Tag.objects.get(name=tag)
                obj.tags.add(t)
            else:
                t = Tag.objects.create(name=tag)
                t.save()
                obj.tags.add(t)

        return obj


class SignupForm(forms.ModelForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    field_order = [
        'username',
        'email',
        'nickname',
        'password',
        'repeat_password',
        'avatar'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)
        avatar = self.cleaned_data['avatar']
        obj = super().save(commit=False)

        obj.user = user
        if commit:
            obj.save()

        return obj

    def clean_password(self):
        password = self.data['password']
        repeat_password = self.data['repeat_password']

        if password != repeat_password:
            self.add_error('password', 'Passwords do not match.')
            self.add_error('repeat_password', 'Passwords do not match.')
        return password

    def clean_username(self):
        username = self.data['username']
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'User with such name already exists.')
        return username


class SettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    field_order = [
        'username',
        'email',
        'nickname',
        'avatar'
    ]

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = self.profile
        profile.user.username = self.cleaned_data['username']
        profile.user.email = self.cleaned_data['email']
        profile.user.save()
        profile.nickname = self.cleaned_data['nickname']
        profile.avatar = self.cleaned_data['avatar']
        profile.save()

        return profile

    def clean_username(self):
        username = self.data['username']
        if username != self.profile.user.username and User.objects.filter(username=username).exists():
            self.add_error('username', 'User with such name already exists.')
        return username


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
        }

    def __init__(self, profile, question, *args, **kwargs):
        self.profile = profile
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.author = self.profile
        obj.question = self.question
        if commit:
            obj.save()

        return obj
