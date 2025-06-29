from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CakeSubmission, Order
from .forms import CakeSubmissionForm, OrderForm

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

def order_cake(request):
    """
    View for customers to place cake orders
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(
                request, 
                f'Thank you for your order, {order.customer_name}! '
                f'We\'ve received your request for a {order.get_cake_flavor_display()} cake. '
                f'We\'ll contact you at {order.customer_email} within 24 hours to confirm your order and provide a quote.'
            )
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OrderForm()
    
    return render(request, 'about/order.html', {'form': form})

@login_required
def my_orders(request):
    """
    View for authenticated users to see their order history
    """
    # Get orders where the customer email matches the logged-in user's email
    user_orders = Order.objects.filter(customer_email=request.user.email).order_by('-order_date')
    
    return render(request, 'about/my_orders.html', {
        'orders': user_orders,
        'user_email': request.user.email
    })