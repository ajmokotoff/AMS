from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# DB Tables below
class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    multiplier = models.DecimalField(decimal_places=2, max_digits=10, default=1)

    def __str__(self):
        return self.ticker


class Portfolio(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Holdings(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=3, max_digits=10)

    # To ensure that these act as primary keys
    class Meta:
        unique_together = (('portfolio', 'stock'))

    def __str__(self):
        return self.portfolio.name + " " + self.stock.ticker


class Transaction(models.Model):
    holdings = models.ForeignKey(Holdings, on_delete=models.CASCADE, default=1)
    quantity = models.DecimalField(decimal_places=3, max_digits=10)

    def __str__(self):
        return str(self.quantity)


# Idea is that this would allow you to view portfolio on a historical date and update prices as this table changes
class StockPrices(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField(default=0)
    price = models.IntegerField(default=0)
    multiplier = models.DecimalField(decimal_places=2, max_digits=10)


# Trigger to update holdings when there is a transaction
@receiver(post_save, sender=Transaction, dispatch_uid="update_holdings_quantity")
def update_quantity(sender, instance, **kwargs):
    instance.holdings.quantity += instance.quantity
    instance.holdings.save()


# Trigger to update stock price when stock price is set
@receiver(post_save, sender=StockPrices, dispatch_uid="update_stock")
def update_price(sender, instance, **kwargs):
    instance.stock.price = instance.price
    instance.stock.multiplier = instance.multiplier
    instance.stock.save()

