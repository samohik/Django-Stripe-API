import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY
domain = "http://127.0.0.1:8000"


class OrderView(DetailView):
    template_name = 'Payment/order.html'
    model = Order
    context_object_name = 'order'

    def get_queryset(self):
        query = super().get_queryset().prefetch_related(
            'items').select_related('discount', 'tax')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = self.get_queryset().first().discount
        coupon = self.coupon_data(data)
        items = self.fill_items()
        checkout_session = self.checkout_session(coupon, items)
        return redirect(checkout_session.url)

    @classmethod
    def checkout_session(cls, coupon, items):
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            automatic_tax={
                'enabled': True,
            },
            mode='payment',
            discounts=[{
                'coupon': coupon
            }],
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return checkout_session

    @classmethod
    def coupon_data(cls, data):
        coupon = stripe.Coupon.create(
            currency=data.currency,
            percent_off=data.percent_off,
            duration=data.duration,
            duration_in_months=data.duration_in_months,
        ).id
        return coupon

    def fill_items(self):
        result = []
        tax = self.get_queryset().first().tax
        items = self.get_queryset().first().items.all()
        for _, item in enumerate(items):
            result.append({
                'price_data': {
                    'currency': 'usd',
                    "tax_behavior": "exclusive",
                    'product_data': {
                        'name': item.name,
                        'tax_code': tax,
                    },
                    'unit_amount_decimal': item.price,
                },
                'quantity': 1,
            })
        return result


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
