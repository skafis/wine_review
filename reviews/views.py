from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Review, Wine
from .forms import ReviewForm, wineForm

from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

def review_list(request, username=None):
    # if not username:
        # username = request.user.username
    latest_review_list = Review.objects.order_by('-pub_date')
    context = {'latest_review_list' :latest_review_list}
    return render(request, 'reviews/review_list.html', context)

def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html',{'review' :review} )
    
def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    latest_review_list = Review.objects.order_by('-pub_date')
    context = {
    'wine_list' : wine_list,
    'latest_review_list' :latest_review_list
    }
    return render(request, 'reviews/wine_list.html', context)

def add_new(request):
    form = wineForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    return render (request, 'reviews/wine_list.html', {'form': form})
    
def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(request, 'reviews/wine_detail.html', {'wine' : wine, })

@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        # user_name = form.cleaned_data['user_name']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))

    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})
    
def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list': latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html',context)