from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Vinyl, Rating
from .forms import VinylForm, RatingForm
from django.db.models import Avg
from .models import Order
from .models import SpotifyNews
from .models import ConcertReminder
from .forms import ConcertReminderForm



# Stránky pro všechny

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# Registrace a přihlášení

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
        else:
            messages.error(request, 'Registrace se nezdařila. Zkontrolujte data.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('vinyl_list')
        else:
            messages.error(request, 'Špatné jméno nebo heslo')
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


# Vinyly a košík 

@login_required(login_url='login')
def vinyl_list(request):
    vinyls = Vinyl.objects.all()
    return render(request, 'vinyl_list.html', {'vinyls': vinyls})

@login_required(login_url='login')
@login_required(login_url='login')
def add_vinyl(request):
    if request.method == "POST":
        form = VinylForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("vinyl_list")
    else:
        form = VinylForm()

    return render(request, "add_vinyl.html", {"form": form})

@login_required(login_url='login')
def add_to_cart(request, vinyl_id):
    if request.method == "POST":
        vinyl = get_object_or_404(Vinyl, id=vinyl_id)
        cart = request.session.get('cart', {})

        cart[str(vinyl_id)] = cart.get(str(vinyl_id), 0) + 1
        request.session['cart'] = cart
        request.session.modified = True

        messages.success(request, f"{vinyl.title} byl přidán do košíku!")
        return redirect('view_cart')
    else:
        return redirect('vinyl_list')
    

@login_required(login_url='login')
def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for vinyl_id, quantity in cart.items():
        vinyl = Vinyl.objects.get(id=vinyl_id)
        total += vinyl.price * quantity
        items.append({'vinyl': vinyl, 'quantity': quantity})

    return render(request, 'cart.html', {
        'cart_items': items,
        'total_price': total
    })

@login_required(login_url='login')
def remove_from_cart(request, vinyl_id):
    cart = request.session.get('cart', {})
    vinyl_id = str(vinyl_id)
    if vinyl_id in cart:
        del cart[vinyl_id]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('view_cart')

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Košík je prázdný!")
        return redirect('vinyl_list')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']

      
        total = 0
        for vinyl_id, quantity in cart.items():
            vinyl = Vinyl.objects.get(id=vinyl_id)
            total += vinyl.price * quantity

        #Admin objednávky
        Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            address=address,
            total_price=total
        )

        # Vyčištění košíku
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(
            request,
            f"Děkujeme, {name}! Vaše objednávka byla úspěšně dokončena ❤️"
        )
        return redirect('order_success')

    return render(request, 'checkout.html', {'cart': cart})


@login_required(login_url='login')
def order_success(request):
    return render(request, 'order_success.html')

#Hodnocení
@login_required
def add_rating(request, vinyl_id):
    vinyl = get_object_or_404(Vinyl, id=vinyl_id)
    if request.method == 'POST':
        stars = int(request.POST.get('stars', 0))
        if stars > 0:
            Rating.objects.create(
                vinyl=vinyl,
                user=request.user,
                stars=stars
            )
            messages.success(request, f"Díky za hodnocení {stars} ⭐!")
        return redirect('vinyl_list')


#about
def about(request):
    return render(request, 'about.html')


#View-hodnocení
def vinyl_list(request):
    vinyls = Vinyl.objects.all()
    return render(request, 'vinyl_list.html', {'vinyls': vinyls})


#Privacy policy
def privacy(request):
    return render(request, 'store/privacy.html')


#Search bar
@login_required(login_url='login')
def vinyl_list(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "")

    vinyls = Vinyl.objects.all()

    # vyhledávání
    if query:
        vinyls = vinyls.filter(title__icontains=query)

    # řazení
    if sort == "title_asc":
        vinyls = vinyls.order_by("title")
    elif sort == "title_desc":
        vinyls = vinyls.order_by("-title")
    elif sort == "price_asc":
        vinyls = vinyls.order_by("price")
    elif sort == "price_desc":
        vinyls = vinyls.order_by("-price")

    return render(request, "vinyl_list.html", {
        "vinyls": vinyls,
        "query": query,
        "sort": sort,
    })
#Edit tlačítko 
@login_required(login_url='login')
def edit_vinyl(request, vinyl_id):
    vinyl = get_object_or_404(Vinyl, id=vinyl_id)

    if request.method == "POST":
        form = VinylForm(request.POST, request.FILES, instance=vinyl)
        if form.is_valid():
            form.save()
            messages.success(request, "Vinyl byl úspěšně upraven!")
            return redirect('vinyl_list')
    else:
        form = VinylForm(instance=vinyl)

    return render(request, 'edit_vinyl.html', {'form': form, 'vinyl': vinyl})

#Nahled vinylu 

def vinyl_detail(request, pk):
    vinyl = get_object_or_404(Vinyl, pk=pk)
    return render(request, 'vinyl_detail.html', {'vinyl': vinyl})


#Seřazení 
def vinyl_list(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "")

    vinyls = Vinyl.objects.all()

    if query:
        vinyls = vinyls.filter(title__icontains=query)

    if sort == "price_asc":
        vinyls = vinyls.order_by("price")
    elif sort == "price_desc":
        vinyls = vinyls.order_by("-price")

    context = {
        "vinyls": vinyls,
        "query": query,
        "sort": sort,
    }

    return render(request, "vinyl_list.html", context)

#Recenze
def vinyl_detail(request, pk):
    vinyl = get_object_or_404(Vinyl, pk=pk)
    ratings = vinyl.ratings.select_related("user").order_by("-created_at")

    if request.user.is_authenticated:
        if request.method == "POST":
            form = RatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.vinyl = vinyl
                rating.user = request.user
                rating.save()
                return redirect("vinyl_detail", pk=vinyl.pk)
        else:
            form = RatingForm()
    else:
        form = None

    return render(request, "vinyl_detail.html", {
        "vinyl": vinyl,
        "ratings": ratings,
        "form": form
    })

#Košík
def cart_view(request):
    cart_items = [] 
    return render(request, 'store/cart.html', {'cart_items': cart_items})

#Spotify news
@login_required(login_url='login')
def spotify_news_view(request):
    sort = request.GET.get('sort', '-release_date')  
    valid_sorts = ['artist_name', 'song_name', 'release_date', '-release_date']
   
    if sort not in valid_sorts:
        sort = '-release_date'
    
    # Seřazení podle parametru
    news_list = SpotifyNews.objects.all().order_by(sort)

    for news in news_list:
        if news.spotify_link:
            news.embed_link = news.spotify_link.replace('track/', 'embed/track/')
        else:
            news.embed_link = None

    return render(request, 'spotify_news.html', {'news_list': news_list, 'current_sort': sort})

#Oblibené songy

@login_required
def toggle_favorite(request, news_id):
    news = get_object_or_404(SpotifyNews, id=news_id)
    user = request.user

    if user in news.favorited_by.all():
        news.favorited_by.remove(user)
    else:
        news.favorited_by.add(user)

    return redirect('spotify_news') 


@login_required
def my_profile(request):
    favorites = request.user.favorite_tracks.all().order_by('-release_date')


    for news in favorites:
        if news.spotify_link:
            news.embed_link = news.spotify_link.replace('track/', 'embed/track/')
        else:
            news.embed_link = None

    favorites_count = favorites.count()

    return render(request, 'profile.html', {
        'favorites': favorites,
        'favorites_count': favorites_count
    })

#Koncerty
@login_required
def my_profile(request):
    favorites = request.user.favorite_tracks.all().order_by('-release_date')
    for news in favorites:
        if news.spotify_link:
            news.embed_link = news.spotify_link.replace('track/', 'embed/track/')
        else:
            news.embed_link = None

    favorites_count = favorites.count()

    # Concert reminder form
    if request.method == 'POST':
        form = ConcertReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect('my_profile')
    else:
        form = ConcertReminderForm()

    reminders = request.user.concert_reminders.all().order_by('concert_date')

    return render(request, 'profile.html', {
        'favorites': favorites,
        'favorites_count': favorites_count,
        'form': form,
        'reminders': reminders
    })

#Slider vinylů

def home(request):
    vinyls = Vinyl.objects.all().order_by('-created_at')[:10] 
    return render(request, "home.html", {"vinyls": vinyls})
