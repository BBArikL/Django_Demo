import django.contrib.auth.models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from .models import User, ToDoList, Item
from .forms import CreateNewTodoList


# Create your views here.


def index(response: WSGIRequest, id: int):
    us: django.contrib.auth.models.User = User.objects.get(id=id)
    # lists: str = ""  # us.todolist_set.get(id=1)
    # item: str = ""  # lists.item_set.get(id=1)
    if us == response.user:

        if response.method == "POST":
            if response.POST.get("Enregister"):
                for todo_list in us.todolist.all():
                    for item in todo_list.item_set.all():
                        if response.POST.get("t"+str(todo_list.id)+"-"+str(item.id)):
                            item.text = response.POST.get("t"+str(todo_list.id)+"-"+str(item.id))
                        if response.POST.get("c" + str(todo_list.id) + "-" + str(item.id)) == "clicked":
                            item.complete = True
                        else:
                            item.complete = False
                        item.save()

            elif response.POST.get("nouvelleListe"):
                name = response.POST.get("new")

                if len(name) > 2:
                    us.todolist.create(name=name)
                else:
                    print("Invalid input")
            elif response.POST.get("nouvelItem"):
                for todo_lst in us.todolist.all():
                    if response.POST.get("nouvelItem") == "sub" + str(todo_lst.id):
                        text = response.POST.get("new" + str(todo_lst.id))
                        todo_lst.item_set.create(text=text, complete=False)

        return render(response, "demoApp/userInfo.html", {"us": us})  # ""{"name": us.name, "id": us.id}"")
        # return HttpResponse(f"<h1>DemoApp working! Hello {us.name}!</h1><p>{lists.name}</p><p>item 1 = {item.text}")

    return HttpResponseRedirect("/")


def home(response: WSGIRequest):
    return render(response, "demoApp/home.html", {})


def create(response: WSGIRequest):
    if response.method == "POST":
        form = CreateNewTodoList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect(f"/{response.user.id}")
    else:
        form = CreateNewTodoList()

    return render(response, "demoApp/create.html", {"form": form})


def lists(response: WSGIRequest):
    return render(response, "demoApp/list.html", {})