from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid, Comment
from .forms import ListingForm


def index(request):
    # Display all active items. ViewType 0 -> use index text-fields
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isActive=True)[::-1],
        "viewType": 0
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(username, password, user)

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
        # create a new Listing if all the inputs are valid and display it
        if form.is_valid():
            formModel = form.save(commit=False)
            if not formModel.imageURL:
                formModel.imageURL = "https://img.icons8.com/ios/500/" \
                                     "000000/no-image.png"
            formModel.createdBy = request.user
            formModel.currentPrice = formModel.startingPrice
            formModel.save()
            return redirect(details, id = formModel.id)

    return render(request, "auctions/create.html", {
        'form': form
    })


def details(request, id):
    entry = Listing.objects.get(id = id)

    if request.method == "POST":

        # if a bid is placed check it and add it to the database
        if "placeBid" in request.POST.keys() and request.POST["bid"]:
            bidPrice=float(request.POST["bid"])

            if (bidPrice > entry.currentPrice) and \
               (bidPrice > entry.startingPrice):
                newBid = Bid(createdBy=request.user, listing=entry, 
                            bidPrice=bidPrice)
                newBid.save()
                entry.currentPrice = bidPrice
                entry.save()
                messages.success(request, 
                                 "Your bid has been succesfully placed!")
            else: 
                messages.error(request, 
                               "Your bid must be higher the current one!")

        # Add or remove item to the watchlist 
        elif "addToWL" in request.POST.keys():
            if entry in request.user.watchlist.all():
                request.user.watchlist.remove(entry)
            else:
                request.user.watchlist.add(entry)

        # Add comment to the database if made
        elif "comment" in request.POST.keys():
            comment = Comment(createdBy=request.user, 
                              description=request.POST["comment"],
                              listing=entry)
            comment.save()

        # close auction, disable listing and show winner 
        elif "closeAuction" in request.POST.keys():
            entry.isActive = False
            entry.save()
    
    # get highest bidder from database
    if entry.bids.all():
        highestBidder = entry.bids.latest("bidPrice").createdBy
    else:
        highestBidder = "None"

    return render(request, "auctions/details.html", {
        "listing": entry,
        "highestBidder": highestBidder,
    })



def watchlist(request):
    # Display all watchlist items. ViewType 1 -> use watchlist text-fields
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all()[::-1],
        "viewType": 1
    })


def categories(request):
    # create a categories name and icons lookup table for looping 
    categoriesAndIcons = [("Books", "fa-book"), 
                          ("Beauty & Personal Care","fa-hand-holding-medical"),
                          ("Fashion","fa-tshirt"),
                          ("Home & Kitchen","fa-couch"),
                          ("Music, CD's and Viny","fa-record-vinyl"), 
                          ("Sports & Outdoor","fa-running"), 
                          ("Technology","fa-laptop"),
                          ("Other","fa-angle-double-right")]

    return render(request, "auctions/categories.html", {
        "categoriesAndIcons": categoriesAndIcons
    })


def category(request, category):
    # Display all items in a category. ViewType 2 -> use category text-fields
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category)[::-1],
        "viewType": 2,
        "category": category
    })
