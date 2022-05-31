from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from. models import Customer
from. models import Admin
from. models import Product

def index(request):
    latest_product_list = Product.objects.order_by('name')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_product_list': latest_product_list,}
    return HttpResponse(template.render(context, request))
# goes to template aka html

def detail(request, product_id):
    return HttpResponse("You're looking at product %s." % product_id)
# response method (ex. 404)

def collection(request, product_id):
    latest_product_list = Product.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_product_list': latest_product_list,}
    return HttpResponse("This is the first collection" % template.render(context, request))

def buy(request, product_id):
    return HttpResponse("%s has been added to your cart." % product_id)