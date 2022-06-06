from django import forms










class  UserSign(forms.Form):
   email = forms.EmailField(max_length=200, required=True)
   password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
