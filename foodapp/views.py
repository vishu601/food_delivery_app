import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Category, FoodItem, Order, OrderItem, UserProfile

# ==========================================
# 1. PROFILE VIEW
# ==========================================
@login_required
def profile_view(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0
    
    context = {
        'profile': user_profile,
        'cart_count': cart_count,
    }
    return render(request, 'profile.html', context) # Directly loads from templates/

# ==========================================
# 2. HOME VIEW (Premium Frontend Mapping)
# ==========================================
def home(request):
    categories = Category.objects.all() if Category.objects.exists() else []
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    food_items = FoodItem.objects.all()
    
    if search_query:
        food_items = food_items.filter(name__icontains=search_query)
        
    if category_id:
        food_items = food_items.filter(category_id=category_id)
        
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0
    
    context = {
        'categories': categories,
        'food_items': food_items,
        'cart_count': cart_count,
        'selected_category': category_id,
        'search_query': search_query
    }
    return render(request, 'home.html', context) # Safe Global Render Path

# ==========================================
# 3. CART MANAGEMENT VIEWS
# ==========================================
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    cart[item_id_str] = cart.get(item_id_str, 0) + 1
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('home')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = 0
    
    for item_id, quantity in cart.items():
        item = get_object_or_404(FoodItem, id=item_id)
        subtotal = item.price * quantity
        total_amount += subtotal
        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal
        })
        
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_count': sum(cart.values())
    }
    return render(request, 'cart.html', context)

def increase_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        cart[item_id_str] += 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

def decrease_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        if cart[item_id_str] > 1:
            cart[item_id_str] -= 1
        else:
            cart.pop(item_id_str)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        cart.pop(item_id_str)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

# ==========================================
# 4. CHECKOUT & ORDER VIEWS
# ==========================================
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')
        
    cart_items = []
    total_amount = 0
    for item_id, quantity in cart.items():
        item = get_object_or_404(FoodItem, id=item_id)
        subtotal = item.price * quantity
        total_amount += subtotal
        cart_items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        order = Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            total_amount=total_amount
        )
        
        for entry in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=entry['item'],
                quantity=entry['quantity'],
                price=entry['item'].price
            )
            
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('order_success', order_id=order.id)

    context = {
        'total_amount': total_amount,
        'cart_count': sum(cart.values())
    }
    return render(request, 'checkout.html', context)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})

# ==========================================
# 5. CORE AUTH & OTP MANAGEMENT VIEWS
# ==========================================
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def otp_login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not phone or len(phone) != 10:
            return render(request, 'otp_login.html', {'backend_error': 'Bhai, 10 digit ka sahi number dalo!'})
            
        generated_otp = str(random.randint(1000, 9999))
        
        try:
            profile = UserProfile.objects.filter(phone_number=phone).first()
            if not profile:
                username = f"user_{phone}"
                user = User.objects.filter(username=username).first()
                if not user:
                    user = User.objects.create_user(username=username)
                profile = UserProfile.objects.create(user=user, phone_number=phone)
                
            profile.otp = generated_otp
            profile.save()
            
            print("\n" + "🔥" * 20)
            print(f"ZWIGATO OTP FOR {phone} IS: {generated_otp}")
            print("🔥" * 20 + "\n")
            
            request.session['login_phone'] = phone
            return redirect('verify_otp')
            
        except Exception as e:
            return render(request, 'otp_login.html', {'backend_error': f"Database Error: {str(e)}"})
        
    return render(request, 'otp_login.html')

def verify_otp_view(request):
    phone = request.session.get('login_phone')
    if not phone:
        return redirect('login')
        
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        profile = UserProfile.objects.filter(phone_number=phone, otp=user_otp).first()
        
        if profile:
            profile.otp = None
            profile.save()
            
            login(request, profile.user)
            if 'login_phone' in request.session:
                del request.session['login_phone']
            return redirect('home')
        else:
            return render(request, 'verify_otp.html', {'phone': phone, 'error': 'Galat OTP dala bhai! Terminal check karo.'})
            
    return render(request, 'verify_otp.html', {'phone': phone})

def logout_view(request):
    logout(request)
    return redirect('home')