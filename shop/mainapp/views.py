from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout_
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import RegisterForm
from .models import MyUser
from . import models


from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Macbook, Iphone, Category, LatestProducts
from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page(
            'macbook', 'iphone', with_respect_to='macbook'
        )
        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'base.html', context)


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = MyUser(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'myapp/register_page.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect('/')


class ProductDetailView(CategoryDetailMixin, DetailView):


    CT_MODEL_MODEL_CLASS = {
        'Macbook': Macbook,
        'Iphone': Iphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
      

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'




class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    querySet = Category.objects.all()
    conext_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwargs = 'slug'