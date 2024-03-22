from django.shortcuts import render

# Create your views here.
def chatbox(request):
    return render(request, 'chatbox/chatbox.html')