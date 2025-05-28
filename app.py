from flask import Flask, render_template, request, redirect, url_for
from crud import *
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Маршруты для материалов
@app.route('/materials')
def materials_list():
    materials_data = list_materials()
    return render_template('materials.html', materials=materials_data)

@app.route('/materials/add', methods=['GET', 'POST'])
def add_material_route():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        add_material(name, description)
        return redirect(url_for('materials_list'))
    return render_template('add_material.html')

@app.route('/materials/delete/<material_id>')
def delete_material_route(material_id):
    delete_material(material_id)
    return redirect(url_for('materials_list'))

@app.route('/materials/search', methods=['GET', 'POST'])
def search_materials():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        materials_data = find_material(search_term)
        return render_template('materials.html', materials=materials_data)
    return render_template('search_material.html')

# Маршруты для заводов
@app.route('/factories')
def factories_list():
    factories_data = list_factories()
    return render_template('factories.html', factories=factories_data)

@app.route('/factories/add', methods=['GET', 'POST'])
def add_factory_route():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        supplier_id = request.form.get('supplier_id')
        add_factory(name, location, supplier_id)
        return redirect(url_for('factories_list'))
    suppliers_data = list_suppliers()
    return render_template('add_factory.html', suppliers=suppliers_data)

@app.route('/factories/delete/<factory_id>')
def delete_factory_route(factory_id):
    delete_factory(factory_id)
    return redirect(url_for('factories_list'))

# Маршруты для рабочих
@app.route('/workers')
def workers_list():
    workers_data = list_workers()
    return render_template('workers.html', workers=workers_data)

@app.route('/workers/add', methods=['GET', 'POST'])
def add_worker_route():
    if request.method == 'POST':
        name = request.form.get('name')
        factory_id = request.form.get('factory_id')
        add_worker(name, factory_id)
        return redirect(url_for('workers_list'))
    factories_data = list_factories()
    return render_template('add_worker.html', factories=factories_data)

@app.route('/workers/delete/<worker_id>')
def delete_worker_route(worker_id):
    delete_worker(worker_id)
    return redirect(url_for('workers_list'))

# Маршруты для заказов
@app.route('/orders')
def orders_list():
    orders_data = list_orders()
    return render_template('orders.html', orders=orders_data)

@app.route('/orders/add', methods=['GET', 'POST'])
def add_order_route():
    if request.method == 'POST':
        material_id = request.form.get('material_id')
        quantity = int(request.form.get('quantity'))
        add_order(material_id, quantity, datetime.now())
        return redirect(url_for('orders_list'))
    materials_data = list_materials()
    return render_template('add_order.html', materials=materials_data)

@app.route('/orders/delete/<order_id>')
def delete_order_route(order_id):
    delete_order(order_id)
    return redirect(url_for('orders_list'))

# Маршруты для поставщиков
@app.route('/suppliers')
def suppliers_list():
    suppliers_data = list_suppliers()
    return render_template('suppliers.html', suppliers=suppliers_data)

@app.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier_route():
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        add_supplier(name, contact)
        return redirect(url_for('suppliers_list'))
    return render_template('add_supplier.html')

@app.route('/suppliers/delete/<supplier_id>')
def delete_supplier_route(supplier_id):
    delete_supplier(supplier_id)
    return redirect(url_for('suppliers_list'))

if __name__ == '__main__':
    app.run(debug=True) 