from django import forms

class RankingFilterForm(forms.Form):
    RANKING_CHOICES = [
        ('all', 'All Rankings'),
        ('top', 'Top Rankings'),
        ('worst', 'Worst Rankings'),
    ]

    ranking_filter = forms.ChoiceField(
        choices=RANKING_CHOICES,
        label='Filter by Ranking',
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='all',
    )
