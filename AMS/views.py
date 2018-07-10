from django.shortcuts import render
from django.http import HttpResponse
from AMS.models import Portfolio
from AMS.models import Holdings
from django.template import loader
from django.db.models import F, Q
from django.db import connections, models, DEFAULT_DB_ALIAS
from django.db.models import DecimalField, ExpressionWrapper, FloatField


# HTML Form to display portfolio
def index(request):
    return render(request, 'AMS/search_form.html')


# This does an inner join on portfolio and holdings, and then computes market value on the query and appends it
# This also checks if min-market-val was supplied, if it was, filter accordingly
def get_portfolio(request):
    if 'portfolio_name' in request.GET and request.GET['portfolio_name']:
        portfolio_name = request.GET['portfolio_name']

        if 'min_market_value' in request.GET and request.GET['min_market_value']:
            portfolio = Holdings.objects\
                .annotate(market_value=ExpressionWrapper(
                (F('stock__price') * F('quantity')) / F('stock__multiplier'), output_field=FloatField()))\
                .filter(portfolio__name=portfolio_name, market_value__gte=request.GET['min_market_value'])

        else:
            portfolio = Holdings.objects \
                .annotate(market_value=ExpressionWrapper(
                (F('stock__price') * F('quantity')) / F('stock__multiplier'), output_field=FloatField())) \
                .filter(portfolio__name=portfolio_name)

        return render(request, 'AMS/search_results.html',
                      {'portfolio': portfolio, 'query': portfolio_name})
    else:
        return HttpResponse('Please submit a portfolio name')
