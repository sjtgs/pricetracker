from django import forms 

# The Image Form
class PriceScannerForm(forms.Form):
    image = forms.ImageField()
    
