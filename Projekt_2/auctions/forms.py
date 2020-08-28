from django.forms import ModelForm
from .models import Listing


class ListingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set field classes
        attrs = {"class": "form-control"}
        for field in self.fields:
            self.fields[field].widget.attrs.update(attrs)

        # set placeholders
        self.fields["title"].widget.attrs.update(
            {"placeholder": "Choose a Title for your listing"})
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Describe your product"})
        self.fields["price"].widget.attrs.update(
            {"placeholder": "Set a starting price"})
        self.fields["imageURL"].widget.attrs.update(
            {"placeholder": 
            "(Optional) Add a image link to showcase your product"})

        # other attributes
        self.fields["title"].widget.attrs.update({"autofocus": "True"})

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'imageURL', 
                  'category']
        labels = {
            "price": "Starting Price",
            "imageURL": "Image Link"
        }
        

