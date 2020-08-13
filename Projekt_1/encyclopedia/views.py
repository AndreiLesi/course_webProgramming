from django.shortcuts import render
from django.http import HttpResponse
import markdown as md

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    # Check if entry exists
    if name in util.list_entries():
        entryHTML = md.markdown(util.get_entry(name))
    else:
        entryHTML = False

    return render(request, "encyclopedia/entry.html", {
        "entry": entryHTML,
        "title": name
    })

