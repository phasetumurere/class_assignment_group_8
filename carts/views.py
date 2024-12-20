from django.shortcuts import render, redirect, get_object_or_404
from store.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart, CartItem, Variation
from utils.kafka_producer import send_message

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # Get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)

                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=current_user)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create new cart item
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)

                except:
                    pass
        try:
            # Get the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))

        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            # existing_variations -> database
            # current variations -> product_variations
            # item_id -> database
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            print(existing_variation_list)

            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # create new cart item
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

# def add_cart(request, product_id):
#     current_user = request.user
#     product = Product.objects.get(id=product_id)  # Get the product

#     # Kafka message initialization
#     kafka_message = {
#         'event': 'add_to_cart',
#         'user_id': current_user.id if current_user.is_authenticated else None,
#         'product_id': product_id,
#         'quantity': 1,
#         'variations': [],
#     }

#     # If the user is authenticated
#     if current_user.is_authenticated:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key,
#                                                       variation_value__iexact=value)
#                     product_variation.append(variation)
#                     kafka_message['variations'].append({'key': key, 'value': value})
#                 except:
#                     pass

#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, user=current_user)
#             existing_variation_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 existing_variation_list.append(list(existing_variation))
#                 id.append(item.id)

#             if product_variation in existing_variation_list:
#                 index = existing_variation_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#                 kafka_message['quantity'] = item.quantity
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

#         # Send Kafka message
#         send_message('cart-events', kafka_message)
#         return redirect('cart')

#     # If the user is not authenticated
#     else:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key,
#                                                       variation_value__iexact=value)
#                     product_variation.append(variation)
#                     kafka_message['variations'].append({'key': key, 'value': value})
#                 except:
#                     pass
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(cart_id=_cart_id(request))
#         cart.save()

#         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, cart=cart)
#             existing_variation_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 existing_variation_list.append(list(existing_variation))
#                 id.append(item.id)

#             if product_variation in existing_variation_list:
#                 index = existing_variation_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#                 kafka_message['quantity'] = item.quantity
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

#         # Send Kafka message
#         send_message('cart-events', kafka_message)
#         return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()

    except:
        pass
    return redirect('cart')


def remove_cartItem(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # Just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    template_name = 'frontEnd/cart.html'
    return render(request, template_name, context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # Just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    template_name = 'frontEnd/checkout.html'
    return render(request, template_name, context)
