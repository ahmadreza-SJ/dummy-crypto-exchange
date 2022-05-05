from django.db import models
from profiles.models import Profile
# Create your models here.


class MarketTransaction(models.Model):
    buy_asset = models.CharField(blank=False, null=False, max_length=20)
    sell_asset = models.CharField(blank=False, null=False, max_length=20)
    amount_to_sell = models.FloatField(blank=False, null=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if (self.sell_asset == 'btc' and self.amount_to_sell > self.profile.bitcoin_balance) or\
                (self.sell_asset == 'usdt' and self.amount_to_sell > self.profile.tether_balance):
            return
        super(MarketTransaction, self).save(*args, **kwargs)

    def execute(self, btc_price):

        if self.buy_asset == 'usdt':
            self.profile.tether_balance += self.amount_to_sell * btc_price
            self.profile.bitcoin_balance -= self.amount_to_sell
        if self.buy_asset == 'btc':
            self.profile.bitcoin_balance += self.amount_to_sell / btc_price
            self.profile.tether_balance -= self.amount_to_sell

        self.profile.save()


class LimitTransaction(MarketTransaction):
    in_price = models.FloatField(blank=False, null=False)


class SignalTransaction(MarketTransaction):
    in_price = models.FloatField(blank=False, null=False)
    target_price = models.FloatField(blank=False, null=False)
    stop_loss = models.FloatField(blank=False, null=False)


class MarketTransactionHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(blank=False, null=False, max_length=20)
    date = models.DateField(auto_now=False)
    buy_asset = models.CharField(blank=False, null=False, max_length=20)
    sell_asset = models.CharField(blank=False, null=False, max_length=20)
    in_price = models.FloatField(blank=False, null=False)
    close_date = models.DateField(auto_now=False)


class LimitTransactionHistory(MarketTransactionHistory):
    in_triggered = models.BooleanField(default=False)


class SignalTransactionHistory(MarketTransactionHistory):
    target_price = models.FloatField(blank=False, null=False)
    stop_loss_price = models.FloatField(blank=False, null=False)
    in_triggered = models.BooleanField(default=False)
    target_triggered = models.BooleanField(default=False)
    sl_triggered = models.BooleanField(default=False)
