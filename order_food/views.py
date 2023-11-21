from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView
from .forms import OrderForm, ChargeWalletForm, AddFoodForm
from .models import Food, Order, Wallet, User
from django.http import HttpResponse, HttpResponseForbidden
from django.db import transaction
# from sms_service.utility import send_sms
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


def index(request):
    return render(request, "index.html")


@login_required(login_url=reverse_lazy("authentication:login"))
def home(request):
    return render(request, "home.html", context={"user": request.user})


class ChooseFood(LoginRequiredMixin, FormView):
    form_class = OrderForm
    template_name = "order_page.html"
    login_url = reverse_lazy("authentication:login")

    def form_valid(self, form):
        food_name = form.cleaned_data["foods"]
        required_quantity = form.cleaned_data["quantity"]
        selected_food = Food.objects.get(name=food_name)
        food_quantity = selected_food.quantity
        food_price = selected_food.price * required_quantity
        student = User.objects.get(username=self.request.user.username)
        student_wallet = student.wallet
        student_wallet_amount = student_wallet.amount

        if student_wallet.amount < food_price:
            return HttpResponse(f"Wallet amount not enough", status=400)

        if required_quantity > food_quantity:
            return HttpResponse(f"Not enough food for quantity of {required_quantity}", status=400)

        entry = Food.objects.select_for_update().get(name=food_name)
        with transaction.atomic():
            entry.quantity = food_quantity - required_quantity
            student_wallet.amount = student_wallet_amount - food_price
            entry.save()
            student_wallet.save()
            order = Order.objects.create(student=student, total_amount=food_price)
            message = {"id": order.id, "food": food_name, "quantity": required_quantity, "status": "successful"}
            # send_sms(message, student.phone_number)

        return redirect("order_food:order-detail", order_id=order.id)


class OrdersDetail(ListView):
    model = Order
    template_name = "all_orders_detail.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        student_id = self.kwargs["student_id"]
        if request.user.id != int(student_id):
            return HttpResponseForbidden("You don't have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        student_id = self.kwargs["student_id"]
        return Order.objects.filter(student_id=student_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = self.get_queryset()
        return context


class OrderDetail(TemplateView):
    template_name = "order_detail.html"

    def dispatch(self, request, *args, **kwargs):
        order_id = self.kwargs["order_id"]
        if not request.user.orders.filter(id=order_id).exists():
            return HttpResponseForbidden("You don't have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        order_id = self.kwargs["order_id"]
        order = Order.objects.get(id=order_id)

        context = {"order": order}
        return context


class WalletDetail(TemplateView):
    template_name = "wallet_detail.html"

    def dispatch(self, request, *args, **kwargs):
        student_id = self.kwargs["student_id"]
        if request.user.id != int(student_id):
            return HttpResponseForbidden("You don't have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        student_id = self.kwargs["student_id"]
        wallet = Wallet.objects.get(student_id=student_id)

        context = {"wallet": wallet}
        return context


class ChargeWallet(FormView):
    form_class = ChargeWalletForm
    template_name = "charge_wallet.html"

    def dispatch(self, request, *args, **kwargs):
        student_id = self.kwargs["student_id"]
        if request.user.id != int(student_id):
            return HttpResponseForbidden("You don't have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        wallet = Wallet.objects.get(student_id=self.request.user.id)
        wallet.amount += int(form.cleaned_data["amount"])
        wallet.save()
        return redirect("order_food:wallet-detail", student_id=self.request.user.id)


class AddFood(PermissionRequiredMixin, FormView):
    form_class = AddFoodForm
    template_name = "add_food.html"
    permission_required = ("add_food",)

    def form_valid(self, form):
        food = form.save()
        return redirect("order_food:food-detail", food_id=food.id)


class ViewFoodDetail(TemplateView):
    template_name = "food_detail.html"

    def get_context_data(self, **kwargs):
        food_id = self.kwargs["food_id"]
        food = Food.objects.get(id=food_id)

        context = {"food": food}
        return context


class ViewAllFoods(ListView):
    model = Food
    template_name = "all_foods_detail.html"
    paginate_by = 10
    queryset = Food.objects.all()
