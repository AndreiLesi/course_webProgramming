from django.core.paginator import Paginator
import random
from .models import *

def getPaginator(request, data, elements):
    """
    Creates a Paginator object and returns page, previous and next URL in a 
    dictionary format. The inputs are request, and data --> here the posts
    """
    # p = Paginator(Post.objects.order_by("-timestamp"), 10)
    p = Paginator(data, elements)
    page_number = request.GET.get("page", 1)
    page = p.get_page(page_number)
    # Set previous page URL 
    if page.has_previous():
        previousURL = f"?page={page.previous_page_number()}"
    else:
        previousURL = ''
    # Set next page URL 
    if page.has_next():
        nextURL = f"?page={page.next_page_number()}"
    else:
        nextURL = ''

    content = {"page": page, "previousURL": previousURL, "nextURL": nextURL}
    return content


def RateCourses(num_ratings, scores=[2,3,4,5]):
    """
    Used to create dummy ratings for the courses by the admin.
    """
    me = User.objects.get(username="Admin@mail.com")
    courses = Course.objects.all()
    # courses = Course.objects.filter(topic="Programming")

    for i in range(num_ratings):
        rating = Rating()
        rating.rating = random.choice(scores)
        rating.creator = me
        rating.course = random.choice(courses)
        rating.save()
        print(f"{i}: Rated {rating.rating}")


