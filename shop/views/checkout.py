from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from shop.models.cart import Cart
from shop.models.order import Order, OrderProduct
from shop.models.product import get_price


class CheckoutView(TemplateView):
    model = Cart
    template_name = "shop/checkout_view.html"

    # form_class = CheckoutForm

    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")
        # print(cart_id)
        if not cart_id:
            return redirect("cart")
        cart = Cart.objects.get(id=cart_id)
        # print(cart.subtotal)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)

        # context["form"] = self.get_form()
        # user_check_id = request.session.get("user_checkout_id")
        # context['']
        user_checkout = None
        if self.request.user.is_authenticated():
            # user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
            # user_checkout.user = self.request.user
            # user_checkout.save()
            # self.request.session['user_checkout_id'] = user_checkout.id
            context["cart"] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        # print(self.object)
        # form = self.get_form()
        # if form.is_valid():
        # email = form.cleaned_data.get('email')
        cart = self.get_object()
        order = Order(user=cart.user)
        op = list()
        user = self.request.user
        order.order_total = cart.subtotal
        order.save()
        for item in cart.cartitem_set.all():
            product = item.item
            price = get_price(product, user)
            qty = item.quantity
            op = OrderProduct(order=order, product=product, qty=qty, price=price)
            # print(op)
            op.save()
        return HttpResponseRedirect('/checkout/')
        # order.save()

        # try:
        #     cart = self.get_object()
        #     order = Order(user=cart.user)
        #     op = list()
        #     user = self.request.user
        #     order.order_total = cart.subtotal
        #     order.save()
        #     for item in cart.cartitem_set.all():
        #         product = item.item
        #         product_price = get_price(product, user)
        #         qty = item.quantity
        #         order_product = OrderProduct(order=order, product=product, product_quantity=qty,
        #                                      product_price=product_price)
        #         op.append(order_product)
        # order.save()

        # user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
        # request.session['user_checkout_id'] = user_checkout.id
        # print(user_checkout)
        # print(created)
        # print(user_checkout)
        # return self.form_valid(form)
        # return HttpResponseRedirect('/checkout/')
        # except:
        #     pass

        # print(e)
        # return HttpResponse('not ok')
        # return self.form_invalid(form)


def get_success_url(self):
    return reverse("checkout")


def get(self, request, *args, **kwargs):
    get_data = super(CheckoutView, self).get(request, *args, **kwargs)
    # cart = self.get_object()
    # user_checkout_id = request.session.get("user_checkout_id")
    # if user_checkout_id:
    #     user_checkout = UserCheckout.objects.get(id=user_checkout_id)
    #     # billing_address_id = ?
    #     # shipping_address_id = ?
    #     try:
    #         new_order_id = request.session["order_id"]
    #         new_order = Order.objects.get(id=new_order_id)
    #     except:
    #         new_order = Order()
    #         request.session['order_id'] = new_order.id
    #     # new_order.cart = cart
    #     # new_order.user = user_checkout
    #     # new_order.save()
    return get_data
