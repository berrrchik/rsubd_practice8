# Cement Factory Practice

Веб-приложение для управления материалами, заводами, рабочими, заказами и поставщиками цементного завода. Проект используется как учебный стенд для практической работы №4 по дисциплине «Оценка параметров функционирования программных систем» и включает полноценный стек централизованного логирования: `Flask + MySQL + Loki + Promtail + Grafana`.

## Что умеет проект

- управлять материалами, заводами, рабочими, заказами и поставщиками через веб-интерфейс;
- работать с `MySQL` вместо локальной файловой БД;
- автоматически создавать таблицы при старте приложения;
- писать структурированные JSON-логи одновременно в файл и `stdout`;
- собирать логи через `Promtail` по схеме `sidecar`;
- хранить и индексировать логи в `Loki`;
- визуализировать логи и метрики ошибок в `Grafana`;
- генерировать тестовые сценарии с разными HTTP-ошибками для демонстрации и отчёта.

## Технологический стек

| Компонент | Версия | Назначение |
|---|---:|---|
| Python | 3.11 | Основной язык проекта |
| Flask | 3.0.0 | Веб-приложение |
| MySQL | 8.4 | Основная база данных |
| PyMySQL | 1.1.1 | Подключение Python к MySQL |
| Loki | 2.9.0 | Хранение и агрегация логов |
| Promtail | 2.9.0 | Сбор логов из файла |
| Grafana | 10.2.0 | Визуализация логов |
| Docker Compose | 2.x | Локальный запуск всей инфраструктуры |

## Архитектура

- `app.py`— Flask-приложение, маршруты, тестовые error-endpoints, HTTP-логирование.
- `logging_config.py` — JSON-форматтер и настройка логгеров.
- `db_connect.py` — подключение к MySQL и создание таблиц.
- `crud.py` — операции чтения и изменения данных.
- `autofill.py` — заполнение базы тестовыми данными.
- `docker-compose.yml` — запуск приложения, MySQL, Loki, Promtail и Grafana.
- `scripts/simulate_failures.py` — генерация тестовых запросов и ошибок.

## Структура данных

Приложение работает со следующими таблицами:

- `materials` — материалы (`id`, `name`, `description`);
- `suppliers` — поставщики (`id`, `name`, `contact`);
- `factories` — заводы (`id`, `name`, `location`, `supplier_id`);
- `workers` — рабочие (`id`, `name`, `factory_id`);
- `production_orders` — производственные заказы (`id`, `material_id`, `quantity`, `order_date`).

Во внутреннем Python-представлении и шаблонах поле `id` отображается как `_id`, чтобы сохранить совместимость с существующим интерфейсом.

## Требования

Для полного запуска нужны:

- `Docker Desktop` или `Docker Engine` + `docker compose`;
- `Python 3.11+` для локального запуска скриптов;
- `Git` для клонирования репозитория.

Проверка:

```bash
docker --version
docker compose version
python3 --version
git --version
```

## Быстрый запуск в Docker

1. Клонируйте репозиторий:

```bash
git clone <repo-url>
cd cement_factory_practice
```

2. Поднимите всю инфраструктуру:

```bash
docker compose up -d --build
```

3. Проверьте состояние контейнеров:

```bash
docker compose ps
```

4. Проверьте доступность сервисов:

```bash
curl http://localhost:5001/health
curl http://localhost:3100/ready
curl http://localhost:3000
```

5. Заполните базу тестовыми данными:

```bash
docker compose exec log-demo-zaklyakovde python autofill.py
```

При первом старте контейнера приложения тестовые данные заполняются автоматически, если база ещё пустая. Команда выше нужна для повторного ручного перезаполнения базы.

6. Откройте интерфейсы:

- приложение: [http://localhost:5001](http://localhost:5001)
- Grafana: [http://localhost:3000](http://localhost:3000)
- Loki readiness: [http://localhost:3100/ready](http://localhost:3100/ready)

## Локальный запуск без Docker

Подходит, если вы хотите запускать только приложение и Python-скрипты вручную.

1. Создайте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Убедитесь, что `MySQL` уже запущен отдельно и доступны параметры:

- host: `127.0.0.1`
- port: `3306`
- database: `cement_logs_demo`
- user: `app`
- password: `app`

4. Запустите приложение:

```bash
python app.py
```

## Работа с MySQL

База данных создаётся автоматически при старте приложения, а таблицы инициализируются в `db_connect.py`.

Подключение к MySQL внутри контейнера:

```bash
docker compose exec db mysql -uapp -papp cement_logs_demo
```

Проверить, что таблицы созданы:

```bash
docker compose exec db mysql -uapp -papp -e "USE cement_logs_demo; SHOW TABLES;"
```

## Заполнение базы

Локально:

```bash
python3 autofill.py
```

Внутри контейнера:

```bash
docker compose exec log-demo-zaklyakovde python autofill.py
```

Скрипт сначала очищает таблицы, затем создаёт тестовые записи для всех сущностей.

## Логирование

Приложение пишет логи в файл:

```text
/var/log/app/application.log
```

Каждая запись формируется в JSON и содержит поля:

- `timestamp`
- `level`
- `message`
- `module`
- `function`
- `line`
- `logger`
- `author`
- `request_id`
- `method`
- `path`
- `status_code`
- `duration_ms`
- `remote_addr`

Уровень логирования определяется автоматически:

- `200-399` → `INFO`
- `400-499` → `WARNING`
- `500+` → `ERROR`

Пример строки лога:

```json
{
  "timestamp": "2026-04-07T18:45:12.123456+00:00",
  "level": "ERROR",
  "message": "GET /demo/failure -> 500",
  "module": "app",
  "method": "GET",
  "path": "/demo/failure",
  "status_code": 500,
  "duration_ms": 3.24
}
```

Посмотреть последние записи:

```bash
docker compose exec log-demo-zaklyakovde sh -c "tail -n 20 /var/log/app/application.log"
```

## Grafana и LogQL

Datasource `Loki` и dashboard настраиваются автоматически через provisioning.

Базовые `LogQL`-запросы:

```logql
{job="cement-factory-app"}
```

```logql
{job="cement-factory-app", level="ERROR"}
```

```logql
sum by (level) (count_over_time({job="cement-factory-app"}[5m]))
```

`LogQL` вводится в `Grafana Explore`:

1. открыть `Explore`;
2. выбрать datasource `Loki`;
3. вставить запрос;
4. нажать `Run query`.

## Demo endpoints

В приложении добавлены специальные маршруты для генерации разных ошибок:

| Endpoint | Статус | Назначение |
|---|---:|---|
| `/demo/bad-request` | 400 | Некорректный запрос |
| `/demo/auth-failure` | 401 | Ошибка авторизации |
| `/demo/forbidden` | 403 | Запрет доступа |
| `/demo/unprocessable` | 422 | Ошибка валидации |
| `/demo/rate-limit` | 429 | Превышение лимита |
| `/demo/failure` | 500 | Внутренняя ошибка сервера |
| `/demo/unavailable` | 503 | Недоступность сервиса |

## Генерация тестовых ошибок

Скрипт `scripts/simulate_failures.py` поддерживает несколько сценариев:

- `normal`
- `bad-request`
- `auth`
- `forbidden`
- `invalid`
- `unprocessable`
- `rate-limit`
- `failure`
- `unavailable`
- `client-errors`
- `server-errors`
- `all`

Примеры запуска:

```bash
python3 scripts/simulate_failures.py --scenario all
```

```bash
python3 scripts/simulate_failures.py --scenario client-errors
```

```bash
docker compose exec log-demo-zaklyakovde python3 scripts/simulate_failures.py --scenario server-errors
```

Если нужно изменить адрес приложения, можно передать переменную окружения:

```bash
SIMULATE_BASE_URL=http://localhost:5001 python3 scripts/simulate_failures.py --scenario all
```

## Полезные команды

Запуск:

```bash
docker compose up -d --build
```

Статус:

```bash
docker compose ps
```

Логи приложения:

```bash
docker compose logs --no-color log-demo-zaklyakovde
```

Логи Grafana:

```bash
docker compose logs --no-color grafana
```

Остановка:

```bash
docker compose down
```

## Структура проекта

```text
cement_factory_practice/
├── app.py
├── autofill.py
├── crud.py
├── db_connect.py
├── docker-compose.yml
├── docker-entrypoint.sh
├── Dockerfile
├── logging_config.py
├── main.py
├── models.py
├── pretty_print.py
├── requirements.txt
├── scripts/
│   └── simulate_failures.py
├── grafana/
│   └── provisioning/
├── loki/
│   └── loki-config.yml
├── promtail/
│   └── promtail-config.yml
├── templates/
└── README.md
```

## Troubleshooting

- Если приложение не стартует, проверьте `docker compose logs log-demo-zaklyakovde`.
- Если нет логов в Grafana, сначала проверьте `curl http://localhost:3100/ready`.
- Если dashboard пустой, выполните несколько запросов к приложению и затем обновите панель.
- Если база пустая, повторно запустите `autofill.py`.
- Если контейнер приложения unhealthy, проверьте доступность MySQL и переменные `MYSQL_*`.
