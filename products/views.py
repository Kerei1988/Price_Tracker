from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, PriceHistory
from .forms import ProductForms
from django.contrib import messages
from django.core.management import call_command




def home(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    else:
        return render(request, 'products/home.html')


@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'products/list.html', {'products': products})


@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForms(request.POST)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForms()

    return render(request, 'products/add.html', {'form': form})


@login_required
def product_detail(request, id_product):
    product = get_object_or_404(Product, id=id_product, user=request.user)
    history = product.price_history.all().order_by('-created_at')[:10]

    return render(request, 'products/detail.html', {
        'product': product,
         'history':history})


@login_required
def history(request, id_product):
    product = get_object_or_404(Product, id=id_product, user=request.user)
    history = PriceHistory.objects.filter(product=product).order_by('-created_at')[:10]
    return render(request, 'products/history.html', {'product': product, 'history': history})


@login_required
def parse_single_product(request, id_product):
    product = Product.objects.get(id=id_product)
    
    try:

        call_command('parse_prices', product=id_product)
        messages.success(request, f'✅ Товар "{product.name}" успешно пропаршен!')
        
    except Exception as e:
        messages.error(request, f'❌ Ошибка: {str(e)}')
    
    return redirect('product_list')
