from django import forms
from .models import User, Project, Task, Post, Tag


# --- Project Form ---
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
        }

# --- Task Form ---
class TaskForm(forms.ModelForm):
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Assign to",
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'attachment', 'assignee']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task Description', 'rows': 3}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# --- Post Form ---
class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'tag1, tag2'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your post content...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]

        if commit:
            instance.save()
            instance.tags.clear()
            for name in tag_names:
                tag_obj, created = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag_obj)
        return instance
