from django.core.mail import EmailMessage

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from io import StringIO, BytesIO
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.auth.models import User
from openpyxl.styles import Border
from openpyxl.styles import Side
from openpyxl.utils import get_column_letter

from postman.models import Message, STATUS_ACCEPTED
from shop.models.cart import Cart
from shop.models.order import Order, OrderProduct
from openpyxl import Workbook


def as_text(value):
    if value is None:
        return ""
    return str(value)


def order_notification(cart, order, user):
    body = 'Новый заказ от %s #%s.\r\n\r\nИнформация о заказе:\r\n' % (order.added.strftime('%d.%m.%Y %H:%M'), order.id)

    for idx, item in enumerate(cart.cartitem_set.all()):
        product = item.item
        price = product.get_price(user)
        qty = item.quantity
        body += '%s. %s %s, %s шт. x %s руб.., на общую сумму: %s руб.\r\n' % (
            idx + 1, product.sku, product.brand, qty, price, qty * price)
        op = OrderProduct(order=order, item=product, qty=qty, price=price)
        op.save()

    body += '\r\nИтого: %s руб.' % (order.order_total)

    subject = 'Сформирован новый заказ от %s № %s!' % (order.added.strftime("%d.%m.%Y %H:%M"), order.id)
    sender = User.objects.filter(username='admin').first()
    recipient = user
    status = STATUS_ACCEPTED
    message_user = Message(subject=subject, body=body, sender=sender, recipient=recipient, moderation_status=status)
    message_user.save()
    message_admin = Message(subject=subject, body=body, sender=recipient, recipient=sender, moderation_status=status)
    message_admin.save()

    # XLS document
    wb = Workbook()
    ws = wb.active
    ws.title = 'Заказ'

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    # ws['A1'] = 'Новый заказ от %s #%s.\r\n\r\nИнформация о заказе:\r\n' % (order.id, order.added)
    # ws['B1'] = '№ п/п'
    # ws['B2'] = 'Товар'
    # ws['B3'] = 'Брэнд'
    # ws['B4'] = 'Количество'
    # ws['B5'] = 'Цена'
    # ws['B5'] = 'Итого по позиции'
    data = []

    for idx, item in enumerate(cart.cartitem_set.all()):
        product = item.item
        price = product.get_price(user)
        qty = item.quantity
        coordinate = 'B' + str(idx)
        data.append([idx + 1, product.sku, product.brand, qty, price, qty * price])

    # print(data)
    ws.append(['#', 'Товар', 'Брэнд', 'Количество', 'Цена за единицу', 'Цена (общая)'])
    for row in data:
        ws.append(row)
    ws.append(['', '', '', '', 'Итого:', order.order_total])

    row_count = ws.max_row + 1
    column_count = ws.max_column + 1

    for i in range(1, row_count):
        for j in range(1, column_count):
            ws.cell(row=i, column=j).border = thin_border

    ws.column_dimensions["A"].width = 5.0
    ws.column_dimensions["B"].width = 23.0
    ws.column_dimensions["C"].width = 17.0
    ws.column_dimensions["D"].width = 13.0
    ws.column_dimensions["E"].width = 18.0
    ws.column_dimensions["F"].width = 18.0

    # for column_cells in ws.columns:
    #     length = max(len(as_text(cell.value)) for cell in column_cells)
    #     ws.column_dimensions[column_cells[0].column].width = length

    # send_mail(
    #     'Новый заказ',
    #     'Сформирован новый заказ',
    #     'no-reply@avtoresurs.net',
    #     ['o.artemov@gov39.ru'],
    #     fail_silently=False,
    # )

    email = EmailMessage(
        subject,
        body,
        'no-reply@avtoresurs.net',
        ['avtoresurs@mail.ru'],
        ['oleg_a@outlook.com'],
        reply_to=['no-reply@avtoresurs.net'],
        headers={'Message-ID': 'foo'},
    )

    output = BytesIO()
    wb.save(output)

    email.attach('order.xlsx', output.getvalue(), 'application/excel')
    email.send()

    return True


class CheckoutView(TemplateView):
    model = Cart
    template_name = "shop/checkout_view.html"

    # form_class = CheckoutForm

    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")

        if not cart_id:
            return redirect("cart")
        cart = Cart.objects.get(id=cart_id)

        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)

        user_checkout = None
        if self.request.user.is_authenticated():
            context["cart"] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        cart = self.get_object()
        order = Order(user=cart.user)
        # user = self.request.user
        order.order_total = cart.subtotal
        order.save()

        order_notification(cart=cart, order=order, user=self.request.user)

        self.request.session['cart_id'] = None

        return HttpResponseRedirect('/checkout/success/')

class CheckoutSuccessView(TemplateView):
    template_name = "shop/checkout_success_view.html"


def get_success_url(self):
    return reverse("checkout")


def get(self, request, *args, **kwargs):
    get_data = super(CheckoutView, self).get(request, *args, **kwargs)
    return get_data
