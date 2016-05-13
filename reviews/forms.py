from django.forms import ModelForm, Textarea
from reviews.models import Review, Wine

class wineForm(ModelForm):
	class Meta:
		model = Wine
		fields = ['name','description']
		widgets = {
            'description': Textarea(attrs={'cols':40, 'rows':15})
            }
		

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols':40, 'rows':15})
            }