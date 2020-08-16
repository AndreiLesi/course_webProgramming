import logging
import markdown as md
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util

logger = logging.getLogger(__name__)

def index(request):
    if request.method == "POST":
        entry = request.POST.get("entry")
        # Empty search case
        if not request.POST.get("entry"):
            return redirect("index")
        else:
            # Entry found case
            if entry in util.list_entries():
                return redirect("entry", entry=entry)
            else:
                # Entry not found case
                matches = [i for i in util.list_entries() if entry in i]
                return render(request, "encyclopedia/index.html", {
                    "entries": matches})   
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})


def entry(request, entry):
    # Check if entry exists
    if entry in util.list_entries():
        entryHTML = md.markdown(util.get_entry(entry))
    else:
        entryHTML = False

    return render(request, "encyclopedia/entry.html", {
        "entry": entryHTML,
        "title": entry
    })