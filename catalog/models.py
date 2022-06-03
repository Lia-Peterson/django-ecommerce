import datetime
from django.conf import settings

from django.db import models
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import reverse

# Create your models here.
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')

#     def __str__(self):
#        return self.question_text

#     def was_published_recently(self):
#        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        

# class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)

#    def __str__(self):
#        return self.choice_text

class Product(models.Model):
    price = models.FloatField(default=0)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    color = models.CharField(max_length=40) #variants
    size = models.CharField(max_length=40) #variants
    
    def __str__(self):
        return self.name
    
    def add_to_cart(request, pk):
        product = get_object_or_404(Product, pk = pk)
        order_product, created = OrderProduct.objects.get_or_create(
            product = product,
            user = request.user,
            ordered = False
        )
        order_qs = Order.objects.filter(user=request.user, ordered= False)

        if order_qs.exists() : 
            order = order_qs[0]

            if order.product.filter(product__pk = product.pk).exists() :
                order_product.quantity += 1
                order_product.save()
                messages.info(request, "Added quantity Product")
                return redirect("core:product", pk = pk)
            else:
                order.products.add(order_product)
                messages.info(request, "Product added to your cart")
                return redirect ("core:product", pk = pk)
    
    def remove_from_cart(request, pk):
        product = get_object_or_404(Product, pk = pk)
        order_qs = Order.objects.filter(
            user = request.user,
            ordered = False
        )

        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__pk = product.pk).exists():
                order_product = OrderProduct.objects.filter(
                    product = product,
                    user = request.user,
                    ordered = False
                ) [0]
                order_product.delete()
                messages.info(request, "Product \""+order_product.product.product_name+"\" remove your cart")
                return redirect("core:product")
            else:
                messages.info(request, "This Product is not in your cart")
                return redirect("core:product", pk = pk)
        else:
            messages.info(request,"You have not placed an Order")
            return redirect("core:product", pk = pk)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"pk" : self.pk})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"pk" : self.pk})
    
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"pk" : self.pk})

class Customer(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100) #float?
    credit_number = models.IntegerField(default=0)
    password = models.CharField(max_length=100) #float?

    def __str__(self):
        return self.name

class Admin(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100) #float?
    
    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.product.name}"
    
    def get_total_product_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object' : order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You did not make an order.")
            return redirect("/")

class HomeView(ListView):
    model = Product
    template_name = "home.html"

class ProductView(DetailView):
    model = Product
    template_name = "product.html"