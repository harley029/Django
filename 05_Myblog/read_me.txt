1.  При использовании классовых-представлений вместо функцыональных:
    - поменять urls 
        path("", views.post_list, name="post_list"),
    на
        path("", views.PostListView.as_view(), name="post_list"),

    - поменять в list.html строчку с пагинацией
        {% include "pagination.html" with page=posts %}
    на  
        {% include "pagination.html" with page=page_obj %}

    - решить проблему обработки неверных номеров страниц при пагинации
      (методы из функцыонального стиля не подходят)

2.  from django.core.mail import send_mail
    send_mail('Django mail', 'This e-mail was sent with Django.', 'harley029@gmail.com', ['harley029@gmail.com'], fail_silently=False)