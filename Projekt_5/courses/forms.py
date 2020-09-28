from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course
from django import forms


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set required fields
        requiredFields = ['first_name', 'last_name', 'username', 'password1', 
        'password2']
        for field in requiredFields:
            self.fields[field].required = True

        # set placeholders
        self.fields["first_name"].widget.attrs.update({"placeholder": "John"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Doe"})
        self.fields["username"].widget.attrs.update(
            {"placeholder": "JohnDoe@gmail.com"})
        self.fields["password1"].widget.attrs.update({"placeholder": "******"})
        self.fields["password2"].widget.attrs.update({"placeholder": "******"})

        # other attributes
        self.fields["first_name"].widget.attrs.update({"autofocus": "True"})

    class Meta:
        model = User
        
        fields = ['first_name', 'last_name', 'username', 'password1', 
                  'password2']

        
        

class CourseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set field classes
        inputAttrs = {"class": "form-control form-control-lg border border-secondary rounded"}
        for field in self.fields:
            self.fields[field].widget.attrs.update(inputAttrs)


        # self.fields["description"].widget.attrs.update(
        #     {"class": "single-textarea"})

        # set placeholders
        self.fields["title"].widget.attrs.update(
            {"placeholder": "Choose a Title for your course"})
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Describe your course in detail"})
        self.fields["price"].widget.attrs.update(
            {"placeholder": "Set a enrollment price"})
        self.fields["topic"].widget.attrs.update(
            {"placeholder": "Topic"})

        # other attributes
        self.fields["title"].widget.attrs.update({"autofocus": "True"})

    # Add second Image link: if one is provided, override original one
    imageLink = forms.URLField(label="Image Link", required=False, widget=forms.TextInput(attrs={'placeholder': "(Optional) Add a image link to showcase your course"}))

    class Meta:
        model = Course
        # fields =  '__all__'
        exclude = ("creator", "image")
        labels = {
            "price": "Course Price",
        }
