from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import Product, Category, Comment, Rating
from cart.forms import CartAddProductForm
from .forms import CommentForm, RatingForm

OBJECTS_PER_PAGE = 2


def populate_products_add_ratings(products):
    for p in products:
        if p.count_rating:
            total_rating = int(p.total_rating / p.count_rating)
            p.stars = range(total_rating)
            p.empty_stars = range(5 - total_rating)
        else:
            p.stars = range(5)
            p.empty_stars = None
    return products


class IndexView(ListView):
    model = Category
    template_name = "shop/index.html"
    context_object_name = "category_list"

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("q")
        products = Product.objects.all()
        if query:
            products = products.filter(name__contains=query)

        page = self.request.GET.get("page", 1)
        paginator = Paginator(products, OBJECTS_PER_PAGE)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        populate_products_add_ratings(products)
        context["products"] = products
        context["query"] = query

        return context


class CategoryProductView(ListView):
    template_name = "shop/category_products.html"
    context_object_name = "products"
    paginate_by = OBJECTS_PER_PAGE

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs["name"])
        products = self.category.product_set.all()
        populate_products_add_ratings(products)
        return products

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["category_list"] = Category.objects.all()
        context["category"] = self.category
        return context


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product_form = CartAddProductForm()
    category_list = Category.objects.all()
    rating = 0
    # star rating
    if product.count_rating:
        rating = int(product.total_rating / product.count_rating)
        stars = range(rating)
        empty_stars = range(5 - rating)
    else:
        stars = range(5)
        empty_stars = None
    # comments
    comments = product.comment_set.filter(is_active=True).prefetch_related("user")
    # queryset = models.Comment.objects.all().prefetch_related("product", "user")
    likes = product.likes
    form = CommentForm()
    rating_form = RatingForm()
    context = {
        "product": product,
        "category_list": category_list,
        "stars": stars,
        "empty_stars": empty_stars,
        "comments": comments,
        "form": form,
        "cart_product_form": cart_product_form,
        "rating_form": rating_form,
        "rating": rating,
        "likes": likes,
    }
    return render(request, "shop/product_detail.html", context=context)


def about(request):
    category_list = Category.objects.all()
    cart_product_form = CartAddProductForm()
    context = {"category_list": category_list, "cart_product_form": cart_product_form}
    return render(request, "shop/about.html", context=context)


@login_required(login_url=reverse_lazy("account:login"))
@require_POST
def process_comment(request, product_pk=None, comment_pk=None):
    time_delta = datetime.timedelta(seconds=30)

    form = CommentForm(request.POST)
    if form.is_valid():
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)

            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()
        else:

            comment = get_object_or_404(Comment, pk=comment_pk)
            form = CommentForm(request.POST, instance=comment)
            form.save()
            product = comment.product

        # after submin redirect to porduct page
    return redirect(product)  # same as product.get_absolute_url


@login_required(login_url=reverse_lazy("account:login"))
def process_rating(request, product_id):
    print("!!!!!!!!!", product_id)
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    print(Rating.objects.all())
    if not Rating.objects.filter(product=product, user=user).exists():
        print("!!!!!!!!!cscsssssssssssssss")
        form = RatingForm(request.POST)
        if form.is_valid():
            print("!!!!!!!!!cscsssssssssssssss!!!!!!!!!!!!!!!!!!!!!!!!")
            rating_note = form.cleaned_data["rating"]
            product.total_rating += rating_note
            product.count_rating += 1
            product.save()
            Rating.objects.create(product=product, user=user)
    return redirect(product)


@csrf_exempt
def like_product(request):
    product_id = request.POST.get('product_id', None)

    likes = 0
    if product_id:
        product = Product.objects.get(id=int(product_id))
        if product is not None:
            likes = product.likes + 1
            product.likes = likes
            product.save()

    return HttpResponse(likes)
