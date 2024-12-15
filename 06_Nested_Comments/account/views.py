from django.shortcuts import render, redirect
from django.views.generic.edit import FormView

from account.forms import UserRegistrationForm


class RegisterView(FormView):
    template_name = "account/register.html"
    form_class = UserRegistrationForm

    # dispatch предотвращает переход на signup залогиненому пользователю
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="posts")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(
                self.request,
                "account/register_done.html",
            )
        return render(request, self.template_name, context={"form": form})
