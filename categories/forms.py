from django import forms

from .models import Tag

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('tag', 'is_new_tag', 'will_be_used_as_tag', 'category',)