from django.shortcuts import render

def view_products(request):
    # Lógica para mostrar los productos
    return render(request, 'products/view_products.html')

def add_product(request):
    # Lógica para agregar un producto
    return render(request, 'products/add_product.html')
