from django import forms
from .models import Vinyl, Artist, Genre, Rating
from .models import ConcertReminder

class VinylForm(forms.ModelForm):
    artist = forms.CharField(
        label="Interpret",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Napiš jméno interpreta"
        })
    )

    class Meta:
        model = Vinyl
        fields = [
            'title',
            'artist',
            'genres',
            'description',
            'tracklist',
            'price',
            'cover_image',
            'release_year',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tracklist': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '1. Intro\n2. Track name\n3. Another song'
            }),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např. 2022'
            }),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'bio']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        widgets = {
            'stars': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Napiš recenzi…'
            }),
        }


class ConcertReminderForm(forms.ModelForm):
    class Meta:
        model = ConcertReminder
        fields = ['artist_name', 'concert_date']
        widgets = {
            'concert_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'artist_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
