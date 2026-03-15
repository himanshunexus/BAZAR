from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.shops.models import Shop

from .forms import ReviewForm
from .models import Review


@login_required
@require_POST
def add_shop_review(request, shop_slug):
    shop = get_object_or_404(Shop, slug=shop_slug)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.shop = shop
        review.save()
        messages.success(request, 'Review submitted.')
    return redirect('shops:detail', slug=shop_slug)
