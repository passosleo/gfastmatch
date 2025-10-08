from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PlatformChoices(models.TextChoices):
    PLAYSTATION_1 = "PS1", "PlayStation 1"
    PLAYSTATION_2 = "PS2", "PlayStation 2"
    PLAYSTATION_3 = "PS3", "PlayStation 3"
    PLAYSTATION_4 = "PS4", "PlayStation 4"
    PLAYSTATION_5 = "PS5", "PlayStation 5"
    XBOX = "XBOX", "Xbox"
    XBOX_360 = "XBOX360", "Xbox 360"
    XBOX_ONE = "XBOXONE", "Xbox One"
    XBOX_SERIES = "XBOXSERIES", "Xbox Series X/S"
    NINTENDO_SWITCH = "SWITCH", "Nintendo Switch"
    PC = "PC", "PC"
    MOBILE = "MOBILE", "Mobile"


class Match(models.Model):
    game_name = models.CharField(max_length=100)
    platform = models.CharField(
        max_length=20, choices=PlatformChoices.choices, default=PlatformChoices.PC
    )
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

    def time_since_creation(self):
        delta = timezone.now() - self.created_at
        if delta.days > 0:
            return f"há {delta.days} dia{'s' if delta.days > 1 else ''}"
        hours = delta.seconds // 3600
        if hours > 0:
            return f"há {hours} hora{'s' if hours > 1 else ''}"
        minutes = delta.seconds // 60
        if minutes > 0:
            return f"há {minutes} minuto{'s' if minutes > 1 else ''}"
        return "agora mesmo"

    def __str__(self):
        return f"{self.game_name} ({self.get_platform_display()})"


class Player(models.Model):
    match = models.ForeignKey(Match, related_name="players", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("match", "user")

    def __str__(self):
        return f"{self.user.username} in {self.match.game_name}"
