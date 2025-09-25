from django.contrib.auth.models import User
from django.db import models


class Match(models.Model):
    game_name = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)
    max_players = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches")

    @property
    def player_users(self):
        return [p.user for p in self.players.all()]

    def current_players(self):
        return self.players.count()

    def is_full(self):
        return self.current_players() >= self.max_players

    def __str__(self):
        return f"{self.game_name} ({self.platform})"


class Player(models.Model):
    match = models.ForeignKey(Match, related_name="players", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("match", "user")

    def __str__(self):
        return f"{self.user.username} in {self.match.game_name}"
