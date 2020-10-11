from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "audio_player/index.html", {})

def room(request, room_name):
    context = { 'chat_room': room_name }
    return render(request, 'audio_player/room.html', context)