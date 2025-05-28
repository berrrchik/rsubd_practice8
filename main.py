from crud import *
from pretty_print import print_materials, print_factories, print_workers, print_orders, print_suppliers, print_documents
from datetime import datetime

def main_menu():
    while True:
        print("\n--- МЕНЮ ПРОИЗВОДСТВА СТРОЙМАТЕРИАЛОВ ---")
        print("1. Материалы\n2. Заводы\n3. Рабочие\n4. Заказы\n5. Поставщики\n6. Выход")
        choice = input("Выбор: ")

        if choice == '1':
            materials_menu()
        elif choice == '2':
            factories_menu()
        elif choice == '3':
            workers_menu()
        elif choice == '4':
            orders_menu()
        elif choice == '5':
            suppliers_menu()
        elif choice == '6':
            break
        else:
            print("Неверный выбор!")

def materials_menu():
    print("\n1. Добавить материал\n2. Показать\n3. Удалить\n4. Найти\n5. Сортировать")
    c = input("Выбор: ")
    if c == '1':
        add_material(input("Название: "), input("Описание: "))
    elif c == '2':
        print_materials(list_materials())
    elif c == '3':
        delete_material(input("ID: "))
    elif c == '4':
        print_materials(find_material(input("Поиск: ")))
    elif c == '5':
        print_materials(sort_collection(materials, input("Поле: ")))

def factories_menu():
    print("\n1. Добавить завод\n2. Показать\n3. Удалить\n4. Сортировать")
    c = input("Выбор: ")
    if c == '1':
        add_factory(input("Название: "), input("Местоположение: "), input("ID поставщика: "))
    elif c == '2':
        print_factories(list_factories())
    elif c == '3':
        delete_factory(input("ID: "))
    elif c == '4':
        print_factories(sort_collection(factories, input("Поле: ")))

def workers_menu():
    print("\n1. Добавить рабочего\n2. Показать\n3. Удалить\n4. Сортировать")
    c = input("Выбор: ")
    if c == '1':
        add_worker(input("Имя: "), input("ID завода: "))
    elif c == '2':
        print_workers(list_workers())
    elif c == '3':
        delete_worker(input("ID: "))
    elif c == '4':
        print_workers(sort_collection(workers, input("Поле: ")))

def orders_menu():
    print("\n1. Добавить заказ\n2. Показать\n3. Удалить\n4. Сортировать")
    c = input("Выбор: ")
    if c == '1':
        add_order(input("ID материала: "), int(input("Количество: ")), datetime.now())
    elif c == '2':
        print_orders(list_orders())
    elif c == '3':
        delete_order(input("ID: "))
    elif c == '4':
        print_orders(sort_collection(production_orders, input("Поле: ")))

def suppliers_menu():
    print("\n1. Добавить поставщика\n2. Показать\n3. Удалить\n4. Сортировать")
    c = input("Выбор: ")
    if c == '1':
        add_supplier(input("Название: "), input("Контакты: "))
    elif c == '2':
        print_suppliers(list_suppliers())
    elif c == '3':
        delete_supplier(input("ID: "))
    elif c == '4':
        print_suppliers(sort_collection(suppliers, input("Поле: ")))

if __name__ == "__main__":
    main_menu()
