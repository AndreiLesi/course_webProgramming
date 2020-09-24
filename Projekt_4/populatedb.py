from network.models import *
from django.contrib.auth.hashers import make_password

users = ["Donald", "Max", "Andrei", "Amanda", "Martina", "Chelsea", "Alex", "David"]


# for user in users:
#     newUser = User(
#         username = user,
#         password = make_password(user),
#         email = user + "@mail.com"
#     )
#     newUser.save()

for user in users:
    newUser = User.objects.get(username = user)
    newUser.password = make_password(user)
    newUser.save()