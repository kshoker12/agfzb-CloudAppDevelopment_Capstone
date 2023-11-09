from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def simpleMethod(request):
    context = {}
    return render(request, 'djangoapp/static_file.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if (request.method == "GET"):
        return render(request, "djangoapp/about.html", context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/contact.html", context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp: index', context)
    else:
        return render(request, 'djangoapp: index', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp:index', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    if request.method == "GET":
        url = "https://karandeepsho-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {"dealerships":dealerships}
        print(dealerships)
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        
        url = "https://karandeepsho-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review"
        dealer_reviews = get_dealer_reviews_from_cf(url, id = dealer_id)
        dealer_names = ' '.join([dealer.name for dealer in dealer_reviews])
        context["reviews"] = dealer_reviews
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # if request.user.is_authenticated:
    url = "https://karandeepsho-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review"
    review = {
        "time": datetime.utcnow().isoformat(),
        "dealership": dealer_id,
        "review": "This is a awesome car dealer",
        "id": 1, 
        "short_name": "Jack", 
        "name": "Jack the Ripper",
        "purchase": "purchase", 
        "purchase_date": "today", 
        "car_make": "Tesla ", 
        "car_model": "Tesla Model Y", 
        "car_year": 2020
        }
    json_payload = {
        "review":review
    }
    result = post_request(url, payload = json_payload)
    print(result)
    return HttpResponse(result["message"])
# def add_review(request, dealer_id):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             url = "https://karandeepsho-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review"
#             review = {
#                 "time": datetime.utcnow().isoformat(),
#                 "dealership": dealer_id,
#                 "id": request.POST["id"],
#                 "review": request.POST["review"], 
#                 "name": request.POST["name"], 
#                 "purchase": request.POST["purchase"], 
#                 "purchase_date": request.POST["purchase_date"], 
#                 "car_make": request.POST["car_make"], 
#                 "car_model": request.POST["car_model"], 
#                 "car_year": request.POST["car_year"]
#             }
    
#             json_payload = {
#                 "review":review
#              }
#             print(review)
#             result = post_request(url, payload = json_payload)
#             return HttpResponse(result["message"])
#         else: 
#             return redirect("djangoapp:index")
#     else: 
#         return redirect("djangoapp:index")

