import os
import time

import pymysql

MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "cement_logs_demo")
MYSQL_USER = os.environ.get("MYSQL_USER", "app")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "app")


def get_connection(retries: int = 10, delay: int = 2):
    last_error = None
    for _ in range(retries):
        try:
            return pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,
            )
        except pymysql.MySQLError as exc:
            last_error = exc
            time.sleep(delay)
    raise last_error


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    contact VARCHAR(255) NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS materials (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    description TEXT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS factories (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NULL,
                    supplier_id INT NOT NULL,
                    CONSTRAINT fk_factories_supplier
                        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS workers (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    factory_id INT NOT NULL,
                    CONSTRAINT fk_workers_factory
                        FOREIGN KEY (factory_id) REFERENCES factories(id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS production_orders (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    material_id INT NOT NULL,
                    quantity INT NOT NULL,
                    order_date DATETIME NOT NULL,
                    CONSTRAINT fk_orders_material
                        FOREIGN KEY (material_id) REFERENCES materials(id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
        conn.commit()


init_db()
