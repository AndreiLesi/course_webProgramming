from django.core.paginator import Paginator


def getPaginator(request, data):
    """
    Creates a Paginator object and returns page, previous and next URL in a 
    dictionary format. The inputs are request, and data --> here the posts
    """
    # p = Paginator(Post.objects.order_by("-timestamp"), 10)
    p = Paginator(data, 10)
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