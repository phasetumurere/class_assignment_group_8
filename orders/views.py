from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import *
from .forms import *
import datetime
from .models import *
import json
from store.models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside the Payment model
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product model
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear the cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order received email to customer
    mail_subject = 'Thank you for ordering!'
    message = render_to_string('accounts/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(
        mail_subject,  # Subject
        message,  # Message
        settings.EMAIL_HOST_USER,  # Sender
        [to_email]  # Receiver
    )
    send_email.fail_silently = True
    send_email.send()

    # Send order number and payment transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

    # template_name = 'frontEnd/orders/payments.html'
    # return render(request, template_name)


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to zero, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing info inside the Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.district = form.cleaned_data['district']
            data.sector = form.cleaned_data['sector']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')  # 20221201

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            template_name = 'frontEnd/orders/payments.html'
            return render(request, template_name, context)
        else:
            return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        payment = Payment.objects.get(payment_id=transID)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }

        template_name = 'frontEnd/orders/order_complete.html'
        return render(request, template_name, context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

from django.shortcuts import render
from collections import defaultdict
import csv

def total_sales(request):
    csv_file = "orders_export.csv"  # Path to your exported orders CSV
    mapped_data = []
    
    # Read the CSV and map the data
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row['User ID']
            order_total = float(row['Order Total'])
            mapped_data.append((user_id, order_total))

    # Reduce phase: Aggregate totals by user
    reduced_data = defaultdict(float)
    for user_id, order_total in mapped_data:
        reduced_data[user_id] += order_total

    # Convert defaultdict to a regular dictionary
    sales_data = dict(reduced_data)

    # Send results to the template
    return render(request, 'frontEnd/orders/total_sales.html', {'sales_data': sales_data})
