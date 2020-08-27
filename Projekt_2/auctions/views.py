from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()[::-1],
        "viewType": 0
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def create(request):
    form = ListingForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            formModel = form.save(commit=False)
            if not formModel.imageURL:
                formModel.imageURL = "https://img.icons8.com/ios/500/" \
                                     "000000/no-image.png"
            formModel.createdBy = request.user
            formModel.currentPrice = formModel.startingPrice
            formModel.description = formModel.description
            formModel.save()
            return render(request, "auctions/create.html", {
                'form': form
            })

    return render(request, "auctions/create.html", {
        'form': form
    })


def details(request, id):
    entry = Listing.objects.get(id = id)

    if request.method == "POST":
        if "placeBid" in request.POST.keys() and request.POST["bid"]:
            bidPrice=float(request.POST["bid"])

            if (bidPrice > entry.currentPrice) and \
               (bidPrice > entry.startingPrice):
                newBid = Bid(createdBy=request.user, listing=entry, 
                            bidPrice=bidPrice)
                newBid.save()
                entry.currentPrice = bidPrice
                entry.save()
                messages.success(request, "Your bid has been succesfully placed!")
            else: 
                messages.error(request, "Your bid must be higher the current one!")

        elif "addToWL" in request.POST.keys():
            if entry in request.user.watchlist.all():
                request.user.watchlist.remove(entry)
            else:
                request.user.watchlist.add(entry)
    
    highestBid = entry.bids.filter(createdBy=request.user.id)
    if highestBid:
        highestBid = float(max(bid.bidPrice for bid in highestBid))
    return render(request, "auctions/details.html", {
        "listing": entry,
        "highestBid": highestBid,
    })


def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all()[::-1],
        "viewType": 1
    })


def categories(request):
    categoriesAndIcons = [("Books", "fa-book"), 
                          ("Beauty & Personal Care","fa-hand-holding-medical"),
                          ("Fashion","fa-tshirt"),("Home & Kitchen","fa-couch"),
                          ("Music, CD's and Viny","fa-record-vinyl"), 
                          ("Sports & Outdoor","fa-running"), 
                          ("Technology","fa-laptop"),
                          ("Other","fa-angle-double-right")]

    return render(request, "auctions/categories.html", {
        "categoriesAndIcons": categoriesAndIcons
    })


def category(request, category):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category)[::-1],
        "viewType": 2,
        "category": category
    })
