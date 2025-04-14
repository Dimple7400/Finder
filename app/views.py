from django.shortcuts import render,redirect,HttpResponse
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout   
from django.contrib.auth.decorators import login_required

@login_required(login_url='log_in')
def home(request):
    
    return render(request, 'index.html')

def books(request):
    query = request.GET.get('q','')
    books = []
    if query:
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(api_url)
        data = response.json()
        books = data.get('items', [])
    context = {
        "book":books,
        "query":query
    }
    return render(request, 'books.html', context)

def book_details(request, book_id):
    url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
    response = requests.get(url)
    book = {}

    if response.status_code == 200:
        book = response.json()
    return render(request, 'book_details.html', {'book': book})

def get_book_by_id(book_id):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{book_id}')
    return response.json() if response.status_code == 200 else None

def add_to_cart(request, book_id):
    book = get_book_by_id(book_id)
    if book:
        cart = request.session.get('cart', [])
        cart.append({
            'id': book_id,
            'title': book['volumeInfo'].get('title', 'No title'),
            'thumbnail': book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
        })
        request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart': cart})

def delete_cart(request, book_id):
    cart = request.session.get('cart', [])
    # Remove the first item that matches the ID
    cart = [item for item in cart if item['id'] != book_id]
    request.session['cart'] = cart
    return redirect('cart')


PIXABAY_API_KEY = '49619359-f232eb7c6beae251bbb02ecb4'
def images(request):
    query = request.GET.get('query')
    images = []
    if query:
        url = 'https://pixabay.com/api/'
        params = {
            'key': PIXABAY_API_KEY,
            'q': query,
            'image_type': 'photo',
            'per_page': 10
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            images = data['hits']
    return render(request, 'images.html',{'images': images})

def image_details(request, image_id):
    url = f'https://pixabay.com/api/?key={PIXABAY_API_KEY }&id={image_id}'
    response = requests.get(url)
    image = None

    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            image = data['hits'][0]

    return render(request, 'image_details.html', {'image': image})

def sign_up(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not match")
        else:
            my_user=User.objects.create_user(uname,pass1,pass2)
            my_user.save()
            return redirect('log_in')
    return render(request, 'sign_up.html')

def log_in(request):
    if request.method == 'POST':
        uname =request.POST.get("username")
        pass1 = request.POST.get("password")
        user = authenticate(request,username=uname,password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username and password is incorrect!!!")
    return render(request, 'log_in.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

def about(request):
    return render(request, 'about.html')

def contect(request):
    return render(request, 'contect.html')
   
