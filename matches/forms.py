from django import forms

from .models import Match


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["game_name", "platform", "max_players"]
        widgets = {
            "game_name": forms.TextInput(attrs={"class": "form-control"}),
            "platform": forms.Select(attrs={"class": "form-select"}),
            "max_players": forms.NumberInput(attrs={"class": "form-control", "min": 2}),
        }

    def clean_max_players(self):
        max_players = self.cleaned_data.get("max_players")

        if max_players is None:
            raise forms.ValidationError("O campo de número máximo é obrigatório.")

        if max_players < 2:
            raise forms.ValidationError(
                "A partida deve permitir pelo menos 2 jogadores (você e mais 1)."
            )

        return max_players
