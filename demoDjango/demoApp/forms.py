from django import forms


class CreateNewTodoList(forms.Form):
    name = forms.CharField(label="Name", max_length=25)
    check = forms.BooleanField(label="Check", required=False)
