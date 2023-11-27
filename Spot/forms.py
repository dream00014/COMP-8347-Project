from django import forms

from Spot.models import Score


class SpotSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, label='Search for companies')

    min_score = forms.IntegerField(required=False, label='Min Score')
    max_score = forms.IntegerField(required=False, label='Max Score')

    # min_volume = forms.IntegerField(required=False, label='Min Volume')
    # max_volume = forms.IntegerField(required=False, label='Max Volume')
    #
    # min_liquidity = forms.IntegerField(required=False, label='Min Liquidity')
    # max_liquidity = forms.IntegerField(required=False, label='Max Liquidity')
    #
    # min_weekly_visit = forms.IntegerField(required=False, label='Min Weekly Visit')
    # max_weekly_visit = forms.IntegerField(required=False, label='Max Weekly Visit')
    #
    # min_markets = forms.IntegerField(required=False, label='Min Markets')
    # max_markets = forms.IntegerField(required=False, label='Max Markets')
    #
    # min_coins = forms.IntegerField(required=False, label='Min Coins')
    # max_coins = forms.IntegerField(required=False, label='Max Coins')


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']
        labels = {
            'score': 'Your Score'
        }
        widgets = {
            'score': forms.Select(choices=Score.score_choice)
        }

