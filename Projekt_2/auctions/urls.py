from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("details/<int:id>", views.details, name="details")
]


# def details(request, id):
#     print(f"Request id was : {id}")
#     entry = Listing.objects.get(id = id)

#     if request.method == "POST":
#         bidPrice=int(request.POST["bid"])
#         if "placeBid" in request.POST.keys():
#             print(type(bidPrice))
#             print(type(entry.currentPrice))

#             if bidPrice > entry.currentPrice:
#                 newBid = Bid(createdBy=request.user, listing=entry, 
#                             bidPrice=bidPrice)
#                 newBid.save()
#                 entry.currentPrice = bidPrice
#                 entry.save()
#                 messages.success(request, "Your bid has been succesfully placed!")
#             else: 
#                 messages.success(request, "Your bid must be higher the current one!")

#         elif "addToWL" in request.POST.keys():
#             pass

#         # return redirect("details", id=title)

    
#     highestBid = entry.bids.filter(createdBy=request.user.id)
#     return render(request, "auctions/details.html", {
#         "listing": entry,
#         "userBids": highestBid,
#         "id": id
#     })