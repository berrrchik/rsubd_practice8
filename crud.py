from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

from db_connect import get_connection

# Допустимые поля сортировки (имя поля в шаблонах → колонка SQL)
_SORT_COLUMNS = {
    "materials": {"_id": "id", "name": "name", "description": "description"},
    "factories": {"_id": "id", "name": "name", "location": "location", "supplier_id": "supplier_id"},
    "workers": {"_id": "id", "name": "name", "factory_id": "factory_id"},
    "production_orders": {
        "_id": "id",
        "material_id": "material_id",
        "quantity": "quantity",
        "order_date": "order_date",
    },
    "suppliers": {"_id": "id", "name": "name", "contact": "contact"},
}


def _row_material(r) -> dict:
    return {"_id": r["id"], "name": r["name"], "description": r["description"] or ""}


def _row_factory(r) -> dict:
    return {
        "_id": r["id"],
        "name": r["name"],
        "location": r["location"] or "",
        "supplier_id": r["supplier_id"],
        "supplier_name": r.get("supplier_name") or "",
    }


def _row_worker(r) -> dict:
    return {
        "_id": r["id"],
        "name": r["name"],
        "factory_id": r["factory_id"],
        "factory_name": r.get("factory_name") or "",
    }


def _row_order(r) -> dict:
    od = r["order_date"]
    if isinstance(od, datetime):
        od = od.isoformat()
    return {
        "_id": r["id"],
        "material_id": r["material_id"],
        "material_name": r.get("material_name") or "",
        "quantity": r["quantity"],
        "order_date": od,
    }


def _row_supplier(r) -> dict:
    return {"_id": r["id"], "name": r["name"], "contact": r["contact"] or ""}


def add_material(name, description):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO materials (name, description) VALUES (%s, %s)",
                (name, description),
            )
        conn.commit()
        return SimpleNamespace(inserted_id=cur.lastrowid)


def list_materials():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM materials ORDER BY id")
            rows = cur.fetchall()
    return [_row_material(r) for r in rows]


def delete_material(material_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM materials WHERE id = %s", (int(material_id),))
        conn.commit()


def find_material(name):
    pattern = f"%{name}%"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, description FROM materials WHERE LOWER(name) LIKE LOWER(%s)",
                (pattern,),
            )
            rows = cur.fetchall()
    return [_row_material(r) for r in rows]


def add_factory(name, location, supplier_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO factories (name, location, supplier_id) VALUES (%s, %s, %s)",
                (name, location, int(supplier_id)),
            )
        conn.commit()
        return SimpleNamespace(inserted_id=cur.lastrowid)


def list_factories():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    f.id,
                    f.name,
                    f.location,
                    f.supplier_id,
                    s.name AS supplier_name
                FROM factories f
                LEFT JOIN suppliers s ON s.id = f.supplier_id
                ORDER BY f.id
                """
            )
            rows = cur.fetchall()
    return [_row_factory(r) for r in rows]


def delete_factory(factory_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM factories WHERE id = %s", (int(factory_id),))
        conn.commit()


def add_worker(name, factory_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO workers (name, factory_id) VALUES (%s, %s)",
                (name, int(factory_id)),
            )
        conn.commit()
        return SimpleNamespace(inserted_id=cur.lastrowid)


def list_workers():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    w.id,
                    w.name,
                    w.factory_id,
                    f.name AS factory_name
                FROM workers w
                LEFT JOIN factories f ON f.id = w.factory_id
                ORDER BY w.id
                """
            )
            rows = cur.fetchall()
    return [_row_worker(r) for r in rows]


def delete_worker(worker_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM workers WHERE id = %s", (int(worker_id),))
        conn.commit()


def add_order(material_id, quantity, order_date):
    if isinstance(order_date, datetime):
        od = order_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        od = str(order_date)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO production_orders (material_id, quantity, order_date) VALUES (%s, %s, %s)",
                (int(material_id), quantity, od),
            )
        conn.commit()
        return SimpleNamespace(inserted_id=cur.lastrowid)


def list_orders():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    o.id,
                    o.material_id,
                    o.quantity,
                    o.order_date,
                    m.name AS material_name
                FROM production_orders o
                LEFT JOIN materials m ON m.id = o.material_id
                ORDER BY o.id
                """
            )
            rows = cur.fetchall()
    return [_row_order(r) for r in rows]


def delete_order(order_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM production_orders WHERE id = %s", (int(order_id),))
        conn.commit()


def add_supplier(name, contact):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO suppliers (name, contact) VALUES (%s, %s)",
                (name, contact),
            )
        conn.commit()
        return SimpleNamespace(inserted_id=cur.lastrowid)


def list_suppliers():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, contact FROM suppliers ORDER BY id")
            rows = cur.fetchall()
    return [_row_supplier(r) for r in rows]


def delete_supplier(supplier_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM suppliers WHERE id = %s", (int(supplier_id),))
        conn.commit()


def sort_collection(table: str, field: str, reverse=False):
    cols = _SORT_COLUMNS.get(table)
    if not cols:
        return []
    col = cols.get(field, "id")
    order = "DESC" if reverse else "ASC"
    # col из whitelist — безопасно для подстановки
    if table == "materials":
        sql = f"SELECT id, name, description FROM materials ORDER BY {col} {order}"
        parse = _row_material
    elif table == "factories":
        sql = f"""
            SELECT
                f.id,
                f.name,
                f.location,
                f.supplier_id,
                s.name AS supplier_name
            FROM factories f
            LEFT JOIN suppliers s ON s.id = f.supplier_id
            ORDER BY f.{col} {order}
        """
        parse = _row_factory
    elif table == "workers":
        sql = f"""
            SELECT
                w.id,
                w.name,
                w.factory_id,
                f.name AS factory_name
            FROM workers w
            LEFT JOIN factories f ON f.id = w.factory_id
            ORDER BY w.{col} {order}
        """
        parse = _row_worker
    elif table == "production_orders":
        sql = f"""
            SELECT
                o.id,
                o.material_id,
                o.quantity,
                o.order_date,
                m.name AS material_name
            FROM production_orders o
            LEFT JOIN materials m ON m.id = o.material_id
            ORDER BY o.{col} {order}
        """
        parse = _row_order
    elif table == "suppliers":
        sql = f"SELECT id, name, contact FROM suppliers ORDER BY {col} {order}"
        parse = _row_supplier
    else:
        return []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    return [parse(r) for r in rows]


def clear_all():
    """Очистка всех таблиц (для autofill). Порядок с учётом внешних ключей."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("TRUNCATE TABLE production_orders")
            cur.execute("TRUNCATE TABLE workers")
            cur.execute("TRUNCATE TABLE factories")
            cur.execute("TRUNCATE TABLE materials")
            cur.execute("TRUNCATE TABLE suppliers")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
