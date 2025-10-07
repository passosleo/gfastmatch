from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import Match, Player


def match_list(request):
    matches = Match.objects.all().order_by("-created_at")
    return render(request, "matches/match_list.html", {"matches": matches})


@login_required
def create_match(request):
    if request.method == "POST":
        game_name = request.POST["game_name"]
        platform = request.POST["platform"]
        max_players = int(request.POST["max_players"])
        Match.objects.create(
            game_name=game_name,
            platform=platform,
            max_players=max_players,
            owner=request.user,
        )
        return redirect("match_list")
    return render(request, "matches/create_match.html")


@login_required
def update_match(request, match_id):
    match = get_object_or_404(Match, id=match_id, owner=request.user)
    if request.method == "POST":
        match.game_name = request.POST["game_name"]
        match.platform = request.POST["platform"]
        match.max_players = int(request.POST["max_players"])
        match.save()
        return redirect("match_list")
    return render(request, "matches/update_match.html", {"match": match})


@login_required
def join_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if not match.is_full():
        Player.objects.get_or_create(match=match, user=request.user)
    return redirect("match_list")


@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id, owner=request.user)
    match.delete()
    return redirect("match_list")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("match_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
