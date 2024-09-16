Помилка “Method Not Allowed (GET)” на сторінці виходу (logout) виникає через те, що за замовчуванням Django очікує, що вихід користувача буде виконуватися через POST-запит. Використання методу GET для цієї операції є недопустимим заради безпеки (щоб уникнути неавторизованого виходу користувача через випадковий або шкідливий GET-запит).

Щоб вирішити цю проблему, є декілька варіантів:

1. Використання POST-запиту для виходу

Найбільш правильним і безпечним рішенням буде зміна посилання на кнопку виходу, яка використовуватиме форму та POST-запит. Ось як це можна зробити в шаблоні:

У файлі base.html змініть блок меню для виходу:
<ul class="menu">
  {% if request.user.is_authenticated %}
    <li>
      <form method="post" action="{% url 'logout' %}">
        {% csrf_token %}
        <button type="submit">Sign out</button>
      </form>
    </li>
  {% else %}
    <li><a href="{% url 'login' %}">Sign in</a></li>
  {% endif %}
</ul>

2. Налаштування використання GET-запиту (менш бажане)

Якщо ви хочете дозволити виконання виходу через GET-запит (хоч це менш безпечно), ви можете змінити поведінку LogoutView, дозволивши обробку GET-запитів.

Для цього потрібно створити власне представлення для виходу, яке дозволятиме GET-запити:
from django.contrib.auth import views as auth_views
from django.urls import path

class LogoutView(auth_views.LogoutView):
    http_method_names = ['get', 'post']  # Дозволяє використання GET-запиту

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
__________________________________________________________________________________

