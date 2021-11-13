from django import forms
from feed.models import FeedItem


class FeedForm(forms.ModelForm):
    class Meta:
        model = FeedItem
        fields = [
            'comment',
        ]
        widgets = { 'comment': forms.TextInput(attrs={'size': 80})}
