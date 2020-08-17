import logging
import markdown as md
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from . import util
from .forms import newEntryForm


logger = logging.getLogger(__name__)


def index(request):
    if request.method == "POST":
        entry = request.POST.get("entry")
        # Empty search case
        if not entry:
            return redirect("index")
        else:
            # Entry found case
            entriesList = list(map(str.lower, util.list_entries()))
            if entry.lower() in entriesList:
                entry = util.list_entries()[entriesList.index(entry.lower())]
                return redirect("entry", entry=entry)
            else:
                # Entry not found case
                matches = [i for i in entriesList if entry.lower() in i]
                matchIndexes = [entriesList.index(i) for i in matches]
                matches = [util.list_entries()[i] for i in matchIndexes]
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


def newPage(request):
    newEntry = newEntryForm()
    if request.method == "POST":
        newEntry = newEntryForm(request.POST)
        if newEntry.is_valid():
            title = newEntry.cleaned_data["title"]
            description = newEntry.cleaned_data["description"]
            entriesList = list(map(str.lower, util.list_entries()))
            if title.lower() not in entriesList:
                util.save_entry(title,description)
                logger.warning(f"Added {title} to the wiki!")
                return redirect("entry", entry=title)
            else:
                messages.error(request, f"{title} already exists")
                print(f"{title} exits")
                print(util.list_entries())

    return render(request, "encyclopedia/newPage.html", {
        "form": newEntry,
    })

def editPage(request,entry):
    pass

