# ImapMigrate

CLI-инструмент для автоматизированной миграции почтовых ящиков между IMAP-серверами.

ImapMigrate получает список папок исходного почтового ящика, определяет количество сообщений, распределяет папки между параллельными workers и выполняет миграцию через [`imapsync`](https://imapsync.lamiral.info/).

## Возможности

* 🔄 Миграция почтовых ящиков между IMAP-серверами
* 📁 Автоматическое получение списка IMAP-папок
* 📊 Подсчёт сообщений в каждой папке перед миграцией
* ⚡ Параллельная обработка папок
* ⚖️ Балансировка нагрузки между workers по количеству сообщений
* 📈 Отображение общего прогресса через `tqdm`
* 📝 Структурированное логирование через `Loguru`
* 📂 Отдельный лог `imapsync` для каждой папки
* 🛑 Корректная остановка миграции через `Ctrl+C`
* ⚙️ Конфигурация через `.env`
* 🖥️ Управление миграцией через CLI

## Как это работает

Процесс миграции состоит из нескольких этапов:

```text
ImapSync Dry-Run
     │
     ▼
Исходный IMAP
     │
     ▼
Авторизация
     │
     ▼
Получение списка папок
     │
     ▼
Подсчёт сообщений
     │
     ▼
Распределение папок между workers
     │
     ├──────────────┬──────────────┐
     ▼              ▼              ▼
 Worker 1       Worker 2       Worker N
     │              │              │
     ▼              ▼              ▼
 imapsync        imapsync        imapsync
     │              │              │
     └──────────────┴──────────────┘
                    │
                    ▼
               Целевой IMAP
                    |
                    ▼
               Пересчет количества сообщений
```

Перед распределением папки сортируются по количеству сообщений. Каждая следующая папка назначается worker'у с наименьшей текущей нагрузкой.

Например:

```text
Worker 1:  15 000 сообщений
Worker 2:  14 500 сообщений
Worker 3:  14 800 сообщений
```

Следующая крупная папка будет назначена Worker 2.

Это позволяет значительно лучше распределять нагрузку, чем простое распределение одинакового количества папок между workers.

## Требования

* Python 3.11+
* `imapsync`
* Доступ к исходному IMAP-серверу
* Доступ к целевому IMAP-серверу

Python-зависимости:

* `python-dotenv`
* `loguru`
* `tqdm`
* `imapclient`

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/ShipHappensBro/ImapMigrate.git
cd ImapMigrate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Если используется Poetry:

```bash
poetry install
```

Убедитесь, что `imapsync` доступен в корне проекта:

```bash
./imapsync
```

При необходимости сделайте файл исполняемым:

```bash
chmod +x ./imapsync
```

---

Убедитесь, что все зависимости `imapsync` установлены

[Список с инструкциями по установке](https://github.com/imapsync/imapsync/tree/master/INSTALL.d)

---

Запустите dry run

```bash
./imapsync --dry
```

## Конфигурация

Создайте файл `.env` в корне проекта:

```dotenv
SOURCE__SERVER=mail.example.ru
SOURCE__PORT=993
SOURCE__AUTH_USER=example@example.ru
SOURCE__PASSWORD=superpass_source

TARGET__SERVER=mail.example.org
TARGET__PORT=993
TARGET__AUTH_USER=example@example.org
TARGET__PASSWORD=superpass_target
```

### Описание параметров

| Переменная          | Назначение                                    |
|---------------------|-----------------------------------------------|
| `SOURCE__SERVER`    | IMAP-сервер источника                         |
| `SOURCE__PORT`      | IMAP-порт сервера источника                   |
| `SOURCE__AUTH_USER` | Учетная запись имперсонации источника         |
| `SOURCE__PASSWORD`  | Пароль учетной записи имперсонации источника  |
| `TARGET__SERVER`    | IMAP-сервер назначения                        |
| `TARGET__PORT`      | IMAP-порт назначения источника                |
| `TARGET__AUTH_USER` | Учетная запись имперсонации назначения        |
| `TARGET__PASSWORD`  | Пароль учетной записи имперсонации назначения |

> **Важно:** файл `.env` содержит учётные данные и не должен попадать в Git.

## Запуск

Миграция запускается с указанием исходного и целевого пользователя:

```bash
python main.py example@example.ru example@example.org
```

Или через Poetry:

```bash
poetry run python main.py example@example.ru example@example.org
```

Посмотреть справку:

```bash
python main.py --help
```

Пример:

```text
usage: main.py [-h] [--workers WORKERS] [--dry] [--verify] source_user target_user

IMAP mailbox migration

positional arguments:
  source_user        Исходный IMAP пользователь
  target_user        Целевой IMAP пользователь

options:
  -h, --help         show this help message and exit
  --workers WORKERS  Количество рабочих процессов.
  --dry              Включить dry-run
  --verify           Включить проверку количества сообщений между серверами
```

## Логирование

Для вывода используется `Loguru`.

В терминале отображаются основные события:

```text
2026-08-12 16:27:40.123 | INFO    | main:main:40 -
Начинаем миграцию: example@example.ru -> example@example.org

2026-08-12 16:27:41.321 | INFO    | main:main:62 -
Получено папок: 64

2026-08-12 16:27:42.105 | INFO    | imapsync_process:run_imapsync:54 -
Начинаем миграцию папки INBOX (12450 сообщений)

2026-08-12 16:27:48.004 | SUCCESS | imapsync_process:run_imapsync:108 -
Миграция завершена: INBOX
```

Для каждой папки создаётся отдельный лог:

```text
logs/
└── imapsync/
    ├── INBOX.log
    ├── Sent.log
    ├── Drafts.log
    └── 2_ЗАПЧАСТИ_mbox.log
```

В этих файлах сохраняется полный вывод `imapsync`.

## Параллельная миграция

Папки обрабатываются через `ThreadPoolExecutor`.

Количество workers определяется автоматически, но максимально задается через cli:

```python
workers_count = min(len(folders), workers_count)
```

Папки распределяются между workers с учётом количества сообщений.

Например, если есть:

```text
INBOX       20 000
Sent         8 000
Archive      7 000
Drafts       1 000
```

то алгоритм старается распределить их таким образом, чтобы общий объём работы каждого worker был максимально близким.

## Остановка миграции

Для остановки нажмите:

```text
Ctrl+C
```

Приложение устанавливает глобальный stop event и корректно завершает запущенные процессы `imapsync`.

Если процесс не завершается самостоятельно в течение заданного времени, используется принудительное завершение.

## Обработка ошибок

Если `imapsync` завершается с ненулевым кодом возврата, ошибка фиксируется в логах:

```text
ERROR | Ошибка миграции INBOX:
exit code 1. Log: logs/imapsync/INBOX.log
```

Полный вывод `imapsync` при этом сохраняется в соответствующем `.log` файле.

## Безопасность

Учётные данные должны храниться в `.env`.

Обязательно добавьте `.env` в `.gitignore`:

```gitignore
.env
```

Также рекомендуется ограничить права доступа к файлу:

```bash
chmod 600 .env
```

## TODO

[TODO](TODO.md)

## License

This project is licensed under the [MIT License](LICENSE).

The project uses [imapsync](https://imapsync.lamiral.info/), which is distributed under its own license.  
The license and terms of use of `imapsync` apply separately.

See the `imapsync` documentation and license for more information.
