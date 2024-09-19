python manage.py runserver

docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

celery -A myshop worker -l info

stripe login

stripe listen --forward-to localhost:8000/payment/webhook/

docker run -it --rm --name redis -p 6379:6379 redis

brew install weasyprint
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH     # для 1, 3 команди


-------------------------
Ошибку, которую вы видите, вызвана тем, что WeasyPrint не может найти или загрузить необходимые внешние библиотеки, такие как gobject-2.0-0. Эта проблема часто возникает на MacOS, потому что библиотека gobject не установлена по умолчанию и требует установки дополнительных пакетов.

Вот несколько шагов, которые помогут устранить эту проблему:

	1.	Установите Homebrew (если еще не установлен):
Если Homebrew еще не установлен, вы можете установить его, выполнив следующую команду в терминале:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

	2.	Установите необходимые библиотеки через Homebrew:
Установите пакеты, которые требуются WeasyPrint для работы:
brew install pango cairo gobject-introspection
	3.	Переустановите WeasyPrint:
После установки необходимых библиотек рекомендуется переустановить WeasyPrint, чтобы убедиться, что он правильно находит все зависимости:
pip uninstall weasyprint
pip install weasyprint
	4.	Проверьте переменные окружения:
Убедитесь, что переменные окружения настроены правильно. Иногда необходимо явно указать пути к установленным библиотекам:
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"

----------------------------------------------------------------
Ошибка, с которой вы столкнулись, указывает на то, что WeasyPrint не может найти библиотеку gobject-2.0-0, необходимую для работы. Эта проблема характерна для MacOS, где некоторые зависимости могут не устанавливаться по умолчанию.

Вот несколько шагов, которые могут помочь решить эту проблему:

	1.	Установите необходимые библиотеки через Homebrew:
Убедитесь, что Homebrew установлен, и выполните команду для установки всех зависимостей, необходимых для WeasyPrint:
brew install cairo pango gdk-pixbuf libffi
	3.	Проверьте пути поиска библиотек:
Возможно, WeasyPrint не может найти библиотеку gobject-2.0-0, потому что она не находится в стандартных путях поиска. Вы можете указать WeasyPrint путь к библиотекам с помощью переменных окружения:
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
	4.	Создайте или отредактируйте файл .zshrc или .bash_profile (в зависимости от используемой оболочки) для постоянного использования этих переменных окружения:
Откройте файл .zshrc или .bash_profile и добавьте следующие строки:
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
	5. Затем примените изменения:
source ~/.zshrc  # для zsh
source ~/.bash_profile  # для bash

------------------------------------------------------------------
Ошибка, которую вы получили, вызвана неправильным использованием оператора / для объединения строк в пути к файлу стилей в WeasyPrint. В Python оператор / используется для работы с объектами пути (Path), а не для объединения обычных строк.

В вашем случае, проблема возникает в этой строке:
weasyprint.HTML(string=html).write_pdf(
    response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")]
)

settings.STATIC_ROOT — это строка, и вы пытаетесь использовать оператор /, который поддерживается объектами Path из модуля pathlib.

Как исправить:

Используйте функцию os.path.join или преобразуйте settings.STATIC_ROOT в объект Path из модуля pathlib.

Вариант 1: Использование os.path.join:
import os

weasyprint.HTML(string=html).write_pdf(
    response, stylesheets=[weasyprint.CSS(os.path.join(settings.STATIC_ROOT, "css/pdf.css"))]
)

Вариант 2: Использование Path:
from pathlib import Path

weasyprint.HTML(string=html).write_pdf(
    response, stylesheets=[weasyprint.CSS(Path(settings.STATIC_ROOT) / "css/pdf.css")]
)

------------------------------------------------------------------------
исправь эту строку с использованием path: stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]

from pathlib import Path

stylesheets=[weasyprint.CSS(Path(settings.STATIC_ROOT) / 'css/pdf.css')]

-------------------------------------------------------------------------