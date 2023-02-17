import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from .models import Item


class ItemsView(ListView):
    template_name = 'Payment/main.html'
    model = Item
    context_object_name = 'items'


class ItemDetailView(DetailView):
    template_name = 'Payment/item_detail.html'
    model = Item
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        return context


class BuyView(View):
    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs.get('id'))
        stripe.api_key = settings.STRIPE_SECRET_KEY
        domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount_decimal': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = 'Payment/success.html'


class CancelView(TemplateView):
    template_name = 'Payment/cancel.html'



