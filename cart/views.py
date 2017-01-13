from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from shop.models.product import Product
from .models import Cart, CartItem

from django.contrib.auth.forms import AuthenticationForm
# from orders.forms import GuestCheckoutForm
from django.views.generic.edit import FormMixin
from order.models import UserCheckout, Order


class ItemCountView(View):
    """ через json отдает счетчик количества итемов в корзине """

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if not cart_id:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    """ вьюха для корзины с json """
    model = Cart
    template_name = 'cart/view.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(259200)
        cart_id = self.request.session.get("cart_id")
        if not cart_id:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        item_added = False
        cart_item = None
        if item_id:
            item_instance = get_object_or_404(Product, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                # pass
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            if created:
                flash_message = "Товар успешно добавлен в корзину"
                item_added = True
            if delete_item:
                flash_message = "Товар удален из корзины"
                cart_item.delete()
            else:
                if not created:
                    flash_message = "Количество товара в корзине изменено"
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax:
                return HttpResponseRedirect(reverse('cart'))
                # return cart_item.cart.get_absolute_url()
        if request.is_ajax():
            # print(request.GET.get('item'))
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0
            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "flash_message": flash_message,
                "total_items": total_items,
            }
            return JsonResponse(data)

        context = {
            "object": self.get_object(),
        }
        template = self.template_name
        return render(request, template, context)


class CheckoutView(TemplateView):
    model = Cart
    template_name = "cart/checkout_view.html"

    # form_class = CheckoutForm

    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")
        if not cart_id:
            return redirect("cart")
        cart = Cart.objects.get(id=cart_id)
        print(cart.subtotal)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)

        # context["form"] = self.get_form()
        # user_check_id = request.session.get("user_checkout_id")
        # context['']
        user_checkout = None
        if self.request.user.is_authenticated():
            user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
            user_checkout.user = self.request.user
            user_checkout.save()
            self.request.session['user_checkout_id'] = user_checkout.id
            context["cart"] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # form = self.get_form()
        # if form.is_valid():
        # email = form.cleaned_data.get('email')
        try:
            user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
            request.session['user_checkout_id'] = user_checkout.id
            print(user_checkout)
            # return self.form_valid(form)
            return reverse('cart')
        except:
            return reverse('news')
            # return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            # billing_address_id = ?
            # shipping_address_id = ?
            try:
                new_order_id = request.session["order_id"]
                new_order = Order.objects.get(id=new_order_id)
            except:
                new_order = Order()
                request.session['order_id'] = new_order.id
            new_order.cart = cart
            new_order.user = user_checkout
            # new_order.save()

        return get_data
