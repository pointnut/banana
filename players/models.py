from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pointnut.commons import ChoiceInfo
from markets.models import Index, Stock
from strategies.models import Strategy, Signal


class Account(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    primary_budget = models.DecimalField(max_digits=10, decimal_places=0)
    secondary_budget = models.DecimalField(max_digits=10, decimal_places=0)
    is_real = models.BooleanField(default=True)
    has_havister = models.BooleanField(default=False)
    date_bound = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.player}'

    @property
    def as_json_dict(self):
        data = {
            'PrimaryBudget': int(self.primary_budget),
            'SecondaryBudget': int(self.secondary_budget),
            'IsReal': self.is_real,
            'HasHavister': self.has_havister,
            'IsActive': self.is_active
        }
        return data


class Shopping(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shoppings')
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='shoppings')
    date_bound = models.DateTimeField(default=timezone.now)
    date_unbound = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.player} | {self.strategy}'


class Play(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plays')
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='plays')
    date_bound = models.DateTimeField(default=timezone.now)
    date_unbound = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.player} | {self.signal}'


class Trade(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='trades')
    level = models.PositiveSmallIntegerField(default=0)
    position_choice = models.CharField(max_length=1, choices=ChoiceInfo.POSITION_CHOICES, null=True)
    piece = models.PositiveSmallIntegerField(default=0)
    quantity = models.PositiveIntegerField()
    price_opened = models.DecimalField(max_digits=9, decimal_places=2)
    price_closed = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    difference = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    change = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    date_opened = models.DateTimeField(null=True, blank=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    is_manual = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.player} | {self.signal} | {self.position}'

    @property
    def position(self):
        return ChoiceInfo.POSITIONS[self.position_choice]
