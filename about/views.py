from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CakeSubmission
from .forms import CakeSubmissionForm

# Create your views here.
def about(request):
    return render(request, "about/about_me.html")

def wall_of_fame(request):
    cakes = CakeSubmission.objects.filter(approval_status='approved').order_by('-submission_date')
    return render(request, 'about/wall_of_fame.html', {'cakes': cakes})

@login_required
def submit_cake(request):
    """
    View for users to submit their cake pictures (login required)
    """
    if request.method == 'POST':
        form = CakeSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            cake_submission = form.save(commit=False)
            cake_submission.user = request.user
            cake_submission.save()
            messages.success(request, 'Your cake has been submitted for approval! We\'ll review it and add it to the Wall of Fame soon.')
            return redirect('wall_of_fame')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CakeSubmissionForm()
    
    return render(request, 'about/submit_cake.html', {'form': form})