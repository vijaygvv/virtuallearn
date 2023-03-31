from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post, Cart, Order
import datetime, math

from django.db.models import Sum
from django.conf import settings
import stripe

from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView


# @login_required(login_url="/login")
def home(request):
    posts = Post.objects.all().order_by("title")
    if request.user:
        # request.session["cart_count"] = Cart.objects.all().count()
        request.session["cart_count"] = Cart.objects.filter(author__id=request.user.id).count()

    if request.method == "POST":
        
        post_id = request.POST.get("poist-d")
        user_id = request.POST.get("user-id")
        cart_id = request.POST.get("cart-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif cart_id:
            cart = Cart.objects.create(author=request.user, post_id=cart_id)
            cart.save()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass
                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'main/home.html', {"posts": posts})



@login_required(login_url="/login")
def my_post(request):
    posts = Post.objects.filter(author=request.user).order_by("title")

    if request.method == "POST":
        post_id = request.POST.get("post-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()

    return render(request, 'main/my_post.html', {"posts": posts})


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/mypost")
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {"form": form})


@login_required(login_url="/login")
@permission_required("main.change_post", login_url="/login", raise_exception=True)
def edit_post(request, id):
    post = Post.objects.get(id=id)  
    return render(request, 'main/edit_post.html', {"post": post})

@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def update_post(request, id):
    post = Post.objects.get(id=id)  
    form = PostForm(request.POST, instance=post)  
    if form.is_valid():  
        form.save()  
        return redirect("/mypost")  
    return render(request, 'main/edit_post.html', {'post': post})  


@login_required(login_url="/login")
@permission_required("main.delete_post", login_url="/login", raise_exception=True)
def delete_post(request, id):
    data = {}
    post = Post.objects.get(id=id)
    if request.method == "POST":
        post.delete()
        return redirect("/mypost")
    return render(request, 'main/delete_post.html', data)

@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def my_cart(request):
    uid = request.user.id
    cart = Cart.objects.filter(author__id=uid)
    total = 0
    for ct in cart:
        total += ct.post.amount
    # total = Cart.objects.annotate(Sum(author__id=uid))
    # sum = Sale.objects.filter(type='Flour').aggregate(Sum('column'))['column__sum']
    # total = Cart.objects.all().aggregate(Min('price'))
    # Product.objects.all().aggregate(Min('price'))
    if request.user:
        request.session["cart_count"] = Cart.objects.filter(author__id=uid).count()
    
        orders = Cart.objects.filter(author__id=uid)
        my_orders = []
        for order in orders:
            temp_dict = {}
            temp_dict['order_title'] = order.post.title
            temp_dict['order_price'] = str(order.post.amount)
            my_orders.append(temp_dict)
    
        request.session['order_list'] = my_orders

    if request.method == "POST":
        cart_post_id = request.POST.get("cart-post-id")
        place_order = request.POST.get("place-order")
        print(place_order,"------place_order-----------")
        if cart_post_id:
            post = Cart.objects.filter(author__id=uid, post__id=cart_post_id ).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        
        elif place_order:
                for crt in cart:
                    order = Order.objects.create(
                        author = request.user,
                        post = crt.post,
                        address = "hyderabad",
                        phone = 9988776655,
                        created_at=datetime.datetime.now()
                        )
                    print(crt,"-crt---------")
                    order.save()
                cart = Cart.objects.filter(author__id=uid)
                for cart_item in cart:
                    cart_item.delete()

    return render(request, "main/my_cart.html", {'cart': cart, "total":total})

@csrf_exempt
# @login_required(login_url="/login")
# @permission_required("main.add_post", login_url="/login", raise_exception=True)
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    

def charge(request):
    if request.method == "POST":
        charge = stripe.Charge.create(
        )


@login_required(login_url="/login")
@permission_required("main.change_post", login_url="/login", raise_exception=True)
def my_order(request):
    uid = request.user.id
    orders = Order.objects.filter(author__id=uid).order_by("-created_at")
    return render(request, "main/my_order.html", {'orders': orders})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})



@csrf_exempt
# @login_required(login_url="/login")
# @permission_required("main.change_post", login_url="/login", raise_exception=True)
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/mycart/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            orders_list = request.session['order_list']
            line_item=[]
            for order in orders_list:
                temp_dict ={
                            "price_data": {
                                "currency": "inr",
                                "product_data": {"name": order['order_title']},
                                "unit_amount": int(float(order['order_price'])*100),
                            },
                            "quantity" : 1
                            # "customer" : request.user.username
                            }
                line_item.append(temp_dict)
            checkout_session = stripe.checkout.Session.create(
                success_url='http://127.0.0.1:8000/myorder/',
                cancel_url='http://127.0.0.1:8000/mycart/',
                payment_method_types=['card'],
                mode='payment',
                line_items = line_item,

            )

            print(checkout_session,"[[[checkout_session]]]")
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})