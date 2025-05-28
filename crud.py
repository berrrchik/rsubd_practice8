
from models import materials, factories, workers, production_orders, suppliers
from bson import ObjectId

def add_material(name, description):
    return materials.insert_one({"name": name, "description": description})

def list_materials():
    return list(materials.find())

def delete_material(material_id):
    return materials.delete_one({"_id": ObjectId(material_id)})

def find_material(name):
    return list(materials.find({"name": {"$regex": name, "$options": "i"}}))

def add_factory(name, location, supplier_id):
    return factories.insert_one({"name": name, "location": location, "supplier_id": ObjectId(supplier_id)})

def list_factories():
    return list(factories.find())

def delete_factory(factory_id):
    return factories.delete_one({"_id": ObjectId(factory_id)})

def add_worker(name, factory_id):
    return workers.insert_one({"name": name, "factory_id": ObjectId(factory_id)})

def list_workers():
    return list(workers.find())

def delete_worker(worker_id):
    return workers.delete_one({"_id": ObjectId(worker_id)})

def add_order(material_id, quantity, order_date):
    return production_orders.insert_one({"material_id": ObjectId(material_id), "quantity": quantity, "order_date": order_date})

def list_orders():
    return list(production_orders.find())

def delete_order(order_id):
    return production_orders.delete_one({"_id": ObjectId(order_id)})

def add_supplier(name, contact):
    return suppliers.insert_one({"name": name, "contact": contact})

def list_suppliers():
    return list(suppliers.find())

def delete_supplier(supplier_id):
    return suppliers.delete_one({"_id": ObjectId(supplier_id)})

def sort_collection(collection, field, reverse=False):
    return list(collection.find().sort(field, -1 if reverse else 1))
