from django import forms
from .models import Vinyl, Artist, Genre, Rating

class VinylForm(forms.ModelForm):
    class Meta:
        model = Vinyl
        fields = [
            'title',
            'artist',
            'genres',
            'description',
            'tracklist',   
            'price',
            'cover_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tracklist': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '1. Intro\n2. Track name\n3. Another song'
            }),
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
            'stars': forms.NumberInput(attrs={'min': 0, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }

        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars", "comment"]
        widgets = {
            "stars": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Napiš recenzi…"
            }),
        }