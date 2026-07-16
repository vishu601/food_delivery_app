<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, FoodItem
from .models import Category, FoodItem, Order, OrderItem
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import FoodItem, Category, UserProfile
from django.contrib.auth.decorators import login_required








# @login_required lagane se agar koi bina login kiye is page par aayega, toh Django use direct login page par bhej dega
@login_required
def profile_view(request):
    # Logged-in user ki profile database se nikalna
    user_profile = UserProfile.objects.filter(user=request.user).first()
    
    # Cart count nikalna navbar ke liye
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0
    
    context = {
        'profile': user_profile,
        'cart_count': cart_count,
    }
<<<<<<< HEAD
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
        
=======
    return render(request, 'foodapp/profile.html', context)










# 1. Purana Home View (Aise hi rahega)
def home(request):
    categories = Category.objects.all()
    
    # URL se category ID aur search query dono nikalna
    category_id = request.GET.get('category')
    search_query = request.GET.get('search') # Search text pakadne ke liye
    
    food_items = FoodItem.objects.all()
    
    # 1. Agar user ne kuch search kiya hai
    if search_query:
        food_items = food_items.filter(name__icontains=search_query) # Naam me keyword dundhega
        
    # 2. Agar user ne category select ki hai
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
    if category_id:
        food_items = food_items.filter(category_id=category_id)
        
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0
    
    context = {
        'categories': categories,
        'food_items': food_items,
        'cart_count': cart_count,
        'selected_category': category_id,
<<<<<<< HEAD
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

=======
        'search_query': search_query # Frontend par search box me text rokne ke liye
    }
    return render(request, 'foodapp/home.html', context)
# 2. Add to Cart View
def add_to_cart(request, item_id):
    # Session se cart uthao, agar nahi hai toh empty dictionary `{}` banao
    cart = request.session.get('cart', {})
    
    # Item ko cart me add karo ya quantity badhao
    item_id_str = str(item_id)
    if item_id_str in cart:
        cart[item_id_str] += 1
    else:
        cart[item_id_str] = 1
        
    # Session ko wapas save karo
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('home')

# 3. View Cart Page
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
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
<<<<<<< HEAD
    return render(request, 'cart.html', context)
=======
    return render(request, 'foodapp/cart.html', context)

>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee

def increase_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
<<<<<<< HEAD
    if item_id_str in cart:
        cart[item_id_str] += 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

def decrease_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
=======
    
    if item_id_str in cart:
        cart[item_id_str] += 1
        
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail') # Wapas cart page par hi rakhega

# 5. Cart me Quantity kam karne ke liye (-)
def decrease_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
    if item_id_str in cart:
        if cart[item_id_str] > 1:
            cart[item_id_str] -= 1
        else:
<<<<<<< HEAD
            cart.pop(item_id_str)
=======
            cart.pop(item_id_str) # Agar 1 se kam ho toh item delete kar do
            
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

<<<<<<< HEAD
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        cart.pop(item_id_str)
=======
# 6. Item ko Cart se bilkul hatane ke liye (Delete/Remove)
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart.pop(item_id_str)
        
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

<<<<<<< HEAD
# ==========================================
# 4. CHECKOUT & ORDER VIEWS
# ==========================================
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')
=======


# 7. Checkout Page View
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home') # Khali cart me checkout nahi hoga
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
        
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
        
<<<<<<< HEAD
=======
        # 1. Database me Order create karo
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
        order = Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            total_amount=total_amount
        )
        
<<<<<<< HEAD
=======
        # 2. Saare Cart Items ko OrderItem me save karo
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
        for entry in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=entry['item'],
                quantity=entry['quantity'],
                price=entry['item'].price
            )
            
<<<<<<< HEAD
        request.session['cart'] = {}
        request.session.modified = True
=======
        # 3. Order hone ke baad Cart khali kar do
        request.session['cart'] = {}
        request.session.modified = True
        
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
        return redirect('order_success', order_id=order.id)

    context = {
        'total_amount': total_amount,
        'cart_count': sum(cart.values())
    }
<<<<<<< HEAD
    return render(request, 'checkout.html', context)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})

# ==========================================
# 5. CORE AUTH & OTP MANAGEMENT VIEWS
# ==========================================
=======
    return render(request, 'foodapp/checkout.html', context)

# 8. Order Success Page View
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'foodapp/order_success.html', {'order': order})

# 9. Signup View (Naya Account Banane Ke Liye)
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
<<<<<<< HEAD
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
=======
            login(request, user) # Account bante hi login kar do
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'foodapp/signup.html', {'form': form})

# 10. Login View (Purane User Ke Liye)
def login_view(request):
    # Agar user pehle se logged in hai toh home par bhej do
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Direct HTML ke custom inputs se data nikalna
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        
        # Django Auth System se verify karna
        user = authenticate(request, username=u_name, password=p_word)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Agar login fail hua toh error show karne ke liye dummy form object bhejna
            from django.contrib.auth.forms import AuthenticationForm
            return render(request, 'foodapp/login.html', {'form': AuthenticationForm(), 'error': True})
            
    return render(request, 'foodapp/login.html')

# 11. Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee

def otp_login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        phone = request.POST.get('phone')
<<<<<<< HEAD
        if not phone or len(phone) != 10:
            return render(request, 'otp_login.html', {'backend_error': 'Bhai, 10 digit ka sahi number dalo!'})
=======
        
        # Validation: Phone number 10 digit ka hona chahiye
        if not phone or len(phone) != 10:
            return render(request, 'foodapp/otp_login.html', {'backend_error': 'Bhai, 10 digit ka sahi number dalo!'})
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
            
        generated_otp = str(random.randint(1000, 9999))
        
        try:
<<<<<<< HEAD
            profile = UserProfile.objects.filter(phone_number=phone).first()
            if not profile:
                username = f"user_{phone}"
                user = User.objects.filter(username=username).first()
                if not user:
                    user = User.objects.create_user(username=username)
                profile = UserProfile.objects.create(user=user, phone_number=phone)
                
            profile.otp = generated_otp
            profile.save()
            
=======
            # Check karo kya user profile pehle se hai?
            profile = UserProfile.objects.filter(phone_number=phone).first()
            
            if not profile:
                # Agar naya user hai toh user create karo
                username = f"user_{phone}"
                # Pehle check karo is username se koi user pehle se toh nahi bana default wala
                user = User.objects.filter(username=username).first()
                if not user:
                    user = User.objects.create_user(username=username)
                
                profile = UserProfile.objects.create(user=user, phone_number=phone)
                
            # OTP save karo
            profile.otp = generated_otp
            profile.save()
            
            # TERMINAL ME PRINT
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
            print("\n" + "🔥" * 20)
            print(f"ZWIGATO OTP FOR {phone} IS: {generated_otp}")
            print("🔥" * 20 + "\n")
            
            request.session['login_phone'] = phone
            return redirect('verify_otp')
            
        except Exception as e:
<<<<<<< HEAD
            return render(request, 'otp_login.html', {'backend_error': f"Database Error: {str(e)}"})
        
    return render(request, 'otp_login.html')

def verify_otp_view(request):
    phone = request.session.get('login_phone')
    if not phone:
        return redirect('login')
=======
            # Agar database me koi dikkat aayegi toh screen par dikhega
            return render(request, 'foodapp/otp_login.html', {'backend_error': f"Database Error: {str(e)}"})
        
    return render(request, 'foodapp/otp_login.html')

# 2. OTP Verify karne ka logic
def verify_otp_view(request):
    phone = request.session.get('login_phone')
    if not phone:
        return redirect('login') # Agar session me phone nahi hai toh wapas bhej do
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
        
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
<<<<<<< HEAD
            return render(request, 'verify_otp.html', {'phone': phone, 'error': 'Galat OTP dala bhai! Terminal check karo.'})
            
    return render(request, 'verify_otp.html', {'phone': phone})

def logout_view(request):
    logout(request)
    return redirect('home')
=======
            return render(request, 'foodapp/verify_otp.html', {'phone': phone, 'error': 'Galat OTP dala bhai! Terminal check karo dobara.'})
            
    return render(request, 'foodapp/verify_otp.html', {'phone': phone})
>>>>>>> ffc0b11d15974bab4b2e229bd7ed0e3e7bd68cee
