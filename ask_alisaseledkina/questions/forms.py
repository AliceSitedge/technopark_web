from django import forms
from questions.models import Question, Tag


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False,
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

    def clean_title(self):
        data = self.cleaned_data['title']
        if 'bad word' in data:
            self.add_error('title', 'bad word detected!')
        return data
