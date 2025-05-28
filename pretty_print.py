from bson.json_util import dumps

def format_material(material):
    return f"""ID: {material['_id']}
Название: {material['name']}
Описание: {material.get('description', '-')}
{'-' * 30}"""

def format_factory(factory):
    return f"""ID: {factory['_id']}
Название: {factory['name']}
Местоположение: {factory['location']}
Поставщик ID: {factory['supplier_id']}
{'-' * 30}"""

def format_worker(worker):
    return f"""ID: {worker['_id']}
Имя: {worker['name']}
Завод ID: {worker['factory_id']}
{'-' * 30}"""

def format_order(order):
    return f"""ID: {order['_id']}
Материал ID: {order['material_id']}
Количество: {order['quantity']}
Дата заказа: {order['order_date']}
{'-' * 30}"""

def format_supplier(supplier):
    return f"""ID: {supplier['_id']}
Название: {supplier['name']}
Контакты: {supplier['contact']}
{'-' * 30}"""

def print_materials(data):
    for item in data:
        print(format_material(item))

def print_factories(data):
    for item in data:
        print(format_factory(item))

def print_workers(data):
    for item in data:
        print(format_worker(item))

def print_orders(data):
    for item in data:
        print(format_order(item))

def print_suppliers(data):
    for item in data:
        print(format_supplier(item))

def print_documents(docs):
    """Обратная совместимость с предыдущим кодом"""
    collection_formatters = {
        'materials': print_materials,
        'factories': print_factories,
        'workers': print_workers,
        'production_orders': print_orders,
        'suppliers': print_suppliers
    }
    
    # Определяем тип коллекции или используем общий формат
    if docs and len(docs) > 0:
        # Пробуем определить тип коллекции по ключам документа
        if 'name' in docs[0] and 'description' in docs[0]:
            print_materials(docs)
        elif 'name' in docs[0] and 'location' in docs[0]:
            print_factories(docs)
        elif 'name' in docs[0] and 'factory_id' in docs[0]:
            print_workers(docs)
        elif 'material_id' in docs[0] and 'quantity' in docs[0]:
            print_orders(docs)
        elif 'name' in docs[0] and 'contact' in docs[0]:
            print_suppliers(docs)
        else:
            # Общий формат для неизвестных коллекций
            for doc in docs:
                for key, value in doc.items():
                    print(f"{key}: {value}")
                print('-' * 30)
