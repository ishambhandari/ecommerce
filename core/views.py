from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from .models import Item, OrderItem , Order, BillingAddress
from django.utils import timezone
from .forms import CheckoutForm
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create- your views here.

class CheckoutView(View):
    def get(self, *args,**kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
          order = Order.objects.get(user=self.request.user, ordered = False)
          if form.is_valid():
           street_address = form.cleaned_data.get('street_address') 
           apartment_address= form.cleaned_data.get('apartment_address')
           zip = form.cleaned_data.get('zip ')
        # NEED TO ADD FUNCTION TO THESE OBJECTS
        #    same_biling_address= form.cleaned_data.get('same_biling_address')
        #    save_info= form.cleaned_data.get('save_info')
           country = form.cleaned_data.get('country')
           payment_option= form.cleaned_data.get('payment_option')
           billing_address = BillingAddress(
               user=self.request.user,
               street_address = street_address,
               apartment_address = apartment_address,
               country = country,
               zip = zip)
           billing_address.save()
           order.billing_address = billing_address
           order.save()
           #add redirect to the selected payment option
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('core:order-summary')

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')  
    def post(self, *args, **kwargs):
        order = Order.objects.get(user = self.request.user, ordered = False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total()) * 100





    # try:
        charge = stripe.Charge.create(
            amount=amount, # in cents
            currency="usd",
            source=token, # obtained with Stripe.js
        )
        #payment creation
        payment = Payment()
        payment.strip_charge_id = charge['id'] 
        payment.user = self.request.user
        payment.amount =  order.get_total()
        payment.save()
    #assigning the pay to the orders.
        order.ordered = True
        order.payment = payment
        order.save()
        messages.error(self.request, "Your order was successful.")        
        return redirect("/")    
#         except stripe.error.CardError as e:
#         # Since it's a decline, stripe.error.CardError will be caught
#             body = e.json_body
#             err  = body.get('error', {})
#             messages.error(self,request, f"{err.get('message')}")
#         except stripe.error.RateLimitError as e:
#             messages.error(self,request, "Limited Rate error")
#             return redirect("/")
        
#         except stripe.error.InvalidRequestError as e:
#         # Invalid parameters were supplied to Stripe's API
#             messages.error(self,request, "Invalid Parameters")
#             return redirect("/")
        
#         except stripe.error.AuthenticationError as e:
#         # Authentication with Stripe's API failed
#         # (maybe you changed API keys recently)
#             messages.error(self,request, "Authentication error")
#             return redirect("/")
#         except stripe.error.APIConnectionError as e:
#         # Network communication with Stripe failed
#             messages.error(self,request, "Failed to connect")
#             return redirect("/")
#         except stripe.error.StripeError as e:
#         # Display a very generic error to the user, and maybe send
#         # yourself an email
#             messages.error(self,request, f"Opps, Something went wrong. Please try again.")
#             return redirect("/")
#         except Exception as e:
#         # send us email 
#             messages.warning(
#                 self.request, "A serious error occurred. We have been notifed.")
#             return redirect("/")







class HomeView(ListView):
    model = Item
    paginate_by = 7 
    template_name = "home.html"

class ItemDetailView(DetailView):
    model = Item 
    template_name = "product.html"
class OrderSummaryView(LoginRequiredMixin,View):
   def get(self,*args, **kwargs):
       try:
           order = Order.objects.get(user=self.request.user, ordered = False)
           context = {
               'object' : order
           }
           return render(self.request, 'order_summary.html', context)
       except ObjectDoesNotExist:
           messages.error(self.request, "You do not have an active order.")
           return redirect('/')
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item = item,
        user=request.user,
        ordered = False 

    )
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check the order items is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated to your cart.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date= ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added onto your cart.")
        return redirect("core:product")
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check the order items is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
            item = item,
            user=request.user,
            ordered = False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed to your cart.")
        else:
            messages.info(request, "This item was not to your cart.")
            return redirect("core:product", slug=slug)
    else:
        #add a message 
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:order-summary")

@login_required
def remove_one_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)