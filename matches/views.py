from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from matches.forms import MatchForm

from .models import Match, Player


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


def match_list(request):
    matches = Match.objects.all().order_by("-created_at")
    return render(request, "matches/match_list.html", {"matches": matches})


@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    players = match.players.select_related("user").all()
    return render(
        request, "matches/match_detail.html", {"match": match, "players": players}
    )


@login_required
def create_match(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.owner = request.user
            match.save()

            Player.objects.create(match=match, user=request.user)

            return redirect("match_detail", match_id=match.id)
    else:
        form = MatchForm()
    return render(request, "matches/create_match.html", {"form": form})


@login_required
def update_match(request, match_id):
    match = get_object_or_404(Match, id=match_id, owner=request.user)
    if request.method == "POST":
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect("match_list")
    else:
        form = MatchForm(instance=match)
    return render(request, "matches/update_match.html", {"form": form, "match": match})


@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id, owner=request.user)
    match.delete()
    return redirect("match_list")


@login_required
def join_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if not match.is_full():
        Player.objects.get_or_create(match=match, user=request.user)
    return redirect("match_list")


@login_required
def leave_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if match.owner == request.user:
        match.delete()
        return redirect("match_list")

    Player.objects.filter(match=match, user=request.user).delete()
    return redirect("match_detail", match_id=match.id)
