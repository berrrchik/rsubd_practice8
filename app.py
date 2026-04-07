import os
import uuid
from datetime import datetime
from time import perf_counter

from flask import Flask, abort, g, jsonify, redirect, render_template, request, url_for

from crud import (
    add_factory,
    add_material,
    add_order,
    add_supplier,
    add_worker,
    delete_factory,
    delete_material,
    delete_order,
    delete_supplier,
    delete_worker,
    find_material,
    list_factories,
    list_materials,
    list_suppliers,
    sort_collection,
)
from logging_config import configure_logging
from models import factories, materials, production_orders, suppliers, workers

AUTHOR_FULL_NAME = "Закляков Даниил Евгеньевич"
AUTHOR_SHORT = "Закляков Д.Е."
AUTHOR_GROUP = "ИКБО-06-22"

app = Flask(__name__)
logger = configure_logging()


def _status_to_level(status_code: int) -> str:
    if 500 <= status_code:
        return "error"
    if 400 <= status_code:
        return "warning"
    return "info"


def _log_message(method: str, path: str, status_code: int) -> str:
    return f"{method} {path} -> {status_code}"


def log_business_event(level: str, message: str) -> None:
    log_method = getattr(logger, level, logger.info)
    log_method(
        message,
        extra={
            "request_id": getattr(g, "request_id", None),
            "method": getattr(request, "method", None),
            "path": getattr(request, "path", None),
            "status_code": getattr(g, "last_status_code", None),
            "duration_ms": getattr(g, "duration_ms", None),
            "remote_addr": request.remote_addr if request else None,
        },
    )


@app.before_request
def before_request():
    g.start_time = perf_counter()
    g.request_id = str(uuid.uuid4())
    g.last_status_code = None
    g.duration_ms = None


@app.after_request
def after_request(response):
    duration_ms = round((perf_counter() - g.start_time) * 1000, 2)
    g.duration_ms = duration_ms
    g.last_status_code = response.status_code
    log_method = getattr(logger, _status_to_level(response.status_code))
    log_method(
        _log_message(request.method, request.path, response.status_code),
        extra={
            "request_id": g.request_id,
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "remote_addr": request.remote_addr,
        },
    )
    response.headers["X-Request-ID"] = g.request_id
    return response


@app.errorhandler(500)
def internal_error(_error):
    return (
        jsonify(
            {
                "status": "error",
                "message": "Внутренняя ошибка сервера",
                "request_id": getattr(g, "request_id", None),
            }
        ),
        500,
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "cement-factory-log-demo"})


@app.route("/")
def index():
    log_business_event("info", "Открыта главная страница приложения")
    return render_template(
        "index.html",
        author_full_name=AUTHOR_FULL_NAME,
        author_group=AUTHOR_GROUP,
    )


@app.route("/demo/auth-failure")
def demo_auth_failure():
    abort(401, description="Тестовая ошибка авторизации")


@app.route("/demo/bad-request")
def demo_bad_request():
    abort(400, description="Тестовый некорректный запрос")


@app.route("/demo/forbidden")
def demo_forbidden():
    abort(403, description="Тестовый запрет доступа")


@app.route("/demo/unprocessable")
def demo_unprocessable():
    abort(422, description="Тестовая ошибка валидации")


@app.route("/demo/rate-limit")
def demo_rate_limit():
    abort(429, description="Тестовое превышение лимита запросов")


@app.route("/demo/failure")
def demo_failure():
    raise RuntimeError("Тестовая 500 ошибка для практической работы №4")


@app.route("/demo/unavailable")
def demo_unavailable():
    abort(503, description="Тестовая недоступность сервиса")


# Маршруты для материалов
@app.route("/materials")
def materials_list():
    sort_by = request.args.get("sort", "_id")
    reverse = request.args.get("reverse", "false") == "true"
    materials_data = sort_collection(materials, sort_by, reverse)
    log_business_event("info", "Открыт список материалов")
    return render_template(
        "materials.html", materials=materials_data, sort_by=sort_by, reverse=reverse
    )


@app.route("/materials/add", methods=["GET", "POST"])
def add_material_route():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        add_material(name, description)
        log_business_event("info", f"Добавлен материал: {name}")
        return redirect(url_for("materials_list"))
    return render_template("add_material.html")


@app.route("/materials/delete/<material_id>")
def delete_material_route(material_id):
    delete_material(material_id)
    log_business_event("warning", f"Удален материал с id={material_id}")
    return redirect(url_for("materials_list"))


@app.route("/materials/search", methods=["GET", "POST"])
def search_materials():
    if request.method == "POST":
        search_term = request.form.get("search_term", "")
        materials_data = find_material(search_term)
        if materials_data:
            log_business_event("info", f"Выполнен поиск материала: {search_term}")
        else:
            log_business_event(
                "warning", f"Поиск материала не дал результатов: {search_term}"
            )
        return render_template("materials.html", materials=materials_data)
    return render_template("search_material.html")


# Маршруты для заводов
@app.route("/factories")
def factories_list():
    sort_by = request.args.get("sort", "_id")
    reverse = request.args.get("reverse", "false") == "true"
    factories_data = sort_collection(factories, sort_by, reverse)
    log_business_event("info", "Открыт список заводов")
    return render_template(
        "factories.html", factories=factories_data, sort_by=sort_by, reverse=reverse
    )


@app.route("/factories/add", methods=["GET", "POST"])
def add_factory_route():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        supplier_id = request.form.get("supplier_id")
        add_factory(name, location, supplier_id)
        log_business_event("info", f"Добавлен завод: {name}")
        return redirect(url_for("factories_list"))
    suppliers_data = list_suppliers()
    return render_template("add_factory.html", suppliers=suppliers_data)


@app.route("/factories/delete/<factory_id>")
def delete_factory_route(factory_id):
    delete_factory(factory_id)
    log_business_event("warning", f"Удален завод с id={factory_id}")
    return redirect(url_for("factories_list"))


# Маршруты для рабочих
@app.route("/workers")
def workers_list():
    sort_by = request.args.get("sort", "_id")
    reverse = request.args.get("reverse", "false") == "true"
    workers_data = sort_collection(workers, sort_by, reverse)
    log_business_event("info", "Открыт список рабочих")
    return render_template(
        "workers.html", workers=workers_data, sort_by=sort_by, reverse=reverse
    )


@app.route("/workers/add", methods=["GET", "POST"])
def add_worker_route():
    if request.method == "POST":
        name = request.form.get("name")
        factory_id = request.form.get("factory_id")
        add_worker(name, factory_id)
        log_business_event("info", f"Добавлен рабочий: {name}")
        return redirect(url_for("workers_list"))
    factories_data = list_factories()
    return render_template("add_worker.html", factories=factories_data)


@app.route("/workers/delete/<worker_id>")
def delete_worker_route(worker_id):
    delete_worker(worker_id)
    log_business_event("warning", f"Удален рабочий с id={worker_id}")
    return redirect(url_for("workers_list"))


# Маршруты для заказов
@app.route("/orders")
def orders_list():
    sort_by = request.args.get("sort", "_id")
    reverse = request.args.get("reverse", "false") == "true"
    orders_data = sort_collection(production_orders, sort_by, reverse)
    log_business_event("info", "Открыт список заказов")
    return render_template(
        "orders.html", orders=orders_data, sort_by=sort_by, reverse=reverse
    )


@app.route("/orders/add", methods=["GET", "POST"])
def add_order_route():
    if request.method == "POST":
        material_id = request.form.get("material_id")
        quantity = int(request.form.get("quantity"))
        add_order(material_id, quantity, datetime.now())
        log_business_event(
            "info", f"Добавлен заказ для material_id={material_id}, quantity={quantity}"
        )
        return redirect(url_for("orders_list"))
    materials_data = list_materials()
    return render_template("add_order.html", materials=materials_data)


@app.route("/orders/delete/<order_id>")
def delete_order_route(order_id):
    delete_order(order_id)
    log_business_event("warning", f"Удален заказ с id={order_id}")
    return redirect(url_for("orders_list"))


# Маршруты для поставщиков
@app.route("/suppliers")
def suppliers_list():
    sort_by = request.args.get("sort", "_id")
    reverse = request.args.get("reverse", "false") == "true"
    suppliers_data = sort_collection(suppliers, sort_by, reverse)
    log_business_event("info", "Открыт список поставщиков")
    return render_template(
        "suppliers.html", suppliers=suppliers_data, sort_by=sort_by, reverse=reverse
    )


@app.route("/suppliers/add", methods=["GET", "POST"])
def add_supplier_route():
    if request.method == "POST":
        name = request.form.get("name")
        contact = request.form.get("contact")
        add_supplier(name, contact)
        log_business_event("info", f"Добавлен поставщик: {name}")
        return redirect(url_for("suppliers_list"))
    return render_template("add_supplier.html")


@app.route("/suppliers/delete/<supplier_id>")
def delete_supplier_route(supplier_id):
    delete_supplier(supplier_id)
    log_business_event("warning", f"Удален поставщик с id={supplier_id}")
    return redirect(url_for("suppliers_list"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5001")),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
    )
