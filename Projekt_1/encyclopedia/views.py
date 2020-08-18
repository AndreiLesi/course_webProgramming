import random
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
        title = request.POST.get("entry")
        # Empty search input case
        if not title:
            return redirect("index")
        else:
            # Entry found case
            entriesList = list(map(str.lower, util.list_entries()))
            if title.lower() in entriesList:
                title = util.list_entries()[entriesList.index(title.lower())]
                return redirect("entry", title=title)
            else:
                # Entry not found case -> search for case insensitive machtes 
                matches = [i for i in entriesList if title.lower() in i]
                matchIndexes = [entriesList.index(i) for i in matches]
                matches = [util.list_entries()[i] for i in matchIndexes]
                return render(request, "encyclopedia/index.html", {
                    "entries": matches})   

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })


def entry(request, title):
    # Check if entry exists
    if title in util.list_entries():
        entryHTML = md.markdown(util.get_entry(title))
    else:
        entryHTML = False

    return render(request, "encyclopedia/entry.html", {
        "entry": entryHTML,
        "title": title,
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
                return redirect("entry", title=title)
            else:
                messages.error(request, f"{title} already exists")

    return render(request, "encyclopedia/newPage.html", {
        "form": newEntry,
    })


def editPage(request, title):
    newEntry = newEntryForm()
    if request.method == "POST":
        newEntry = newEntryForm(request.POST)
        if newEntry.is_valid():
            print("cleandata POST: ", newEntry.cleaned_data["description"])
            util.save_entry(newEntry.cleaned_data["title"],
                            newEntry.cleaned_data["description"])
            return redirect("entry", title=newEntry.cleaned_data["title"])

    newEntry.fields['title'].initial = title
    newEntry.fields['description'].initial = util.get_entry(title)
    print("Lines here")
    print(util.get_entry(title))
    return render(request, "encyclopedia/editPage.html", {
        "title": title,
        "form": newEntry
    })

