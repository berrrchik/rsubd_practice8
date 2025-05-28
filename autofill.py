from crud import (
    add_material, add_factory, add_worker, 
    add_order, add_supplier
)
from datetime import datetime, timedelta

# Очистка всех коллекций
from models import materials, factories, workers, production_orders, suppliers
materials.delete_many({})
factories.delete_many({})
workers.delete_many({})
production_orders.delete_many({})
suppliers.delete_many({})

print("⚙️  Начинается автозаполнение...")

# Добавляем поставщиков
supplier_ids = []
supplier_ids.append(add_supplier("Global Cement Supplies", "+1-800-555-0199").inserted_id)
supplier_ids.append(add_supplier("Евроцемент Групп", "+7-495-123-4567").inserted_id)
supplier_ids.append(add_supplier("Asian Building Materials", "+86-10-9876-5432").inserted_id)

print("✅ Поставщики добавлены")

# Добавляем заводы
factory_ids = []
factory_ids.append(add_factory("North Cement Plant", "Нью-Йорк", supplier_ids[0]).inserted_id)
factory_ids.append(add_factory("Подмосковный ЖБИ", "Московская область", supplier_ids[1]).inserted_id)
factory_ids.append(add_factory("Shanghai Construction Materials", "Шанхай", supplier_ids[2]).inserted_id)

print("✅ Заводы добавлены")

# Добавляем материалы
material_ids = []
material_ids.append(add_material("Бетон М400", "Высокопрочный бетон для несущих конструкций").inserted_id)
material_ids.append(add_material("Цемент ПЦ500", "Портландцемент марки 500").inserted_id)
material_ids.append(add_material("Щебень гранитный", "Фракция 5-20 мм").inserted_id)
material_ids.append(add_material("Песок строительный", "Речной мытый песок").inserted_id)
material_ids.append(add_material("Арматура", "Стальная арматура 14 мм").inserted_id)

print("✅ Материалы добавлены")

# Добавляем рабочих
worker_ids = []
worker_ids.append(add_worker("Иван Петров", factory_ids[0]).inserted_id)
worker_ids.append(add_worker("John Doe", factory_ids[0]).inserted_id)
worker_ids.append(add_worker("Алексей Смирнов", factory_ids[1]).inserted_id)
worker_ids.append(add_worker("Дмитрий Иванов", factory_ids[1]).inserted_id)
worker_ids.append(add_worker("Li Wei", factory_ids[2]).inserted_id)
worker_ids.append(add_worker("Zhang Min", factory_ids[2]).inserted_id)

print("✅ Рабочие добавлены")

# Добавляем заказы
today = datetime.now()
add_order(material_ids[0], 500, today)
add_order(material_ids[1], 1000, today - timedelta(days=1))
add_order(material_ids[2], 2000, today - timedelta(days=2))
add_order(material_ids[3], 1500, today - timedelta(days=3))
add_order(material_ids[4], 800, today - timedelta(days=4))
add_order(material_ids[0], 750, today - timedelta(days=5))
add_order(material_ids[1], 1200, today - timedelta(days=6))

print("✅ Заказы добавлены")

print("\n🎉 Автозаполнение завершено.")
