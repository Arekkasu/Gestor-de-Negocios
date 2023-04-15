import datetime
import os
import time
import pandas as pd
import random
from termcolor import colored, cprint

Workers_csv = pd.read_csv("Assets/workers.csv")
Products_csv = pd.read_csv("Assets/products.csv", index_col=0)

pd.options.display.max_rows = None

sep = '--------------------------------------------------------------------------'

os.environ["TERM"] = "xterm"
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def actualizar_workers_csv():

    # Se decide llamar la variable correspondiente al dataframe y se le asigna que se lea nuevamente en una variable,
    # permitiendo que se mantega la lectura desde su ultima modificacion y al final con la funcion concat(), se unen los
    # data frames y se genera uno solo

    global Workers_csv
    global Products_csv
    new_data = pd.read_csv('Assets/workers.csv')
    new_data_products = pd.read_csv('Assets/products.csv')
    Products_csv = pd.concat([Products_csv, new_data_products], ignore_index=False)
    Workers_csv = pd.concat([Workers_csv, new_data], ignore_index=True)


# Creacion de contrasena de empleado
def password_worker(name):

    password = str(random.randint(111, 999)) + name[::3]
    return password
# command = 1
def registrar_Empleado(id, name, last_name, second_lastname,sex, age, mobile_number, password, selling_products=0):
    if (Workers_csv['id'] == id).any():
        return cprint(f"El siguiente empleado {name} {last_name}, ya se encuentra registrado\n")
    else:
        with open('Assets/workers.csv', mode='+a') as workers:
            workers.write(f"{id},{name},{last_name},{second_lastname},{sex},{age},{mobile_number},{password},{selling_products}\n")
            workers.close()
        time.sleep(2)
        output = cprint(f"El Empleado con {id} ha sido Registrado Correctamente.\nLa contraseña para el inicio de caja es: {password}\n", "green")

    return output

# command = 2
def registrar_producto(name_product, price, quantity):

    id_product = Products_csv.index[-1]+1

    existencia = existencia_producto(name_product)

    if isinstance(existencia, tuple):
        return False
    else:

        with open('Assets/products.csv', mode = 'a+') as products:
            products.write(f"\n{id_product},{name_product},{price},{quantity}")
            products.close()
        return True


# command = 3
def existencia_producto(found_product):

    """
    Al tener definido como columna de index name_product de products.csv, se usa loc para facilitar encontrar
    el valor de lo que se pide, dataframe.loc[index, columna]
    """

    try:
        id_product = int(found_product)
        if id_product in Products_csv.index:

            price_product = Products_csv.loc[id_product, "price"]
            quantity_product = Products_csv.loc[id_product, "quantity"]
            name = Products_csv.loc[id_product, "name_product"]
            return True, id_product, name, price_product, quantity_product


        else:
            return False
    except:
        name_of_product = Products_csv[Products_csv['name_product'] == found_product]
        if not name_of_product.empty:
            id_product = name_of_product.index[0]
            price_product = name_of_product.loc[id_product, "price"]
            quantity_product = name_of_product.loc[id_product, "quantity"]
            name = name_of_product.loc[id_product, "name_product"]
            return True, id_product, name , price_product, quantity_product
        else:
            return False

# command = 4
def products_list():
    return f"\n{Products_csv}\n"


def start_sales():

    fecha = datetime.date.today().strftime("%d/%m/%Y")
    hora_actual = datetime.datetime.now().strftime("%H:%M")
    #Orden de compra


    lista_compra = {}


    clear_screen()
    while True:
        print(sep)
        print(f"Iniciando proceso de ventas. \nPor favor, ingrese tu {colored(f'usuario', 'green')} y tu {colored(f'contraseña', 'blue')}.")
        print(sep)
        user = int(input(f"Ingrese el numero de Identificacion: "))
        password = str(input(f"Ingrese la contraseña: "))
        if (Workers_csv['id'] == user).any() & (Workers_csv['password'] == password).any():
            clear_screen()
            while True:
                print(f"""\n\t|{"-".center(60, "-")}|{"-".center(60, "-")}|{"-".center(60, "-")}|""")
                print(f"""\t|{colored("Fecha".center(60, "-"), "blue")}|{colored("Hora".center(60, "-"), "blue")}|{colored("ID".center(60, "-"), "blue")}|""")
                print(f"""\t|{colored("-".center(182, "-"), "yellow")}|""")
                #print(f"hora_actual.center(5))
                print(f"""\t|{fecha.center(60, " ")}|{hora_actual.center(60, " ")}|{str(user).center(60, " ")}|""")
                #separador
                print(f"""\t|{"-".center(182, "-")}|""")
                input()
                break
        break



def main():
    clear_screen()
    while True:
        clear_screen()
        cprint("\n------------------------------GESTOR VENTAS----------------------------\n", 'yellow')
        command = input(f"Ingresa un comando, en caso de no conocer un comando ingrese \'{colored('help', 'green', 'on_dark_grey')}\': ").upper()


        """
        OPCION DE REGISTRO DE EMPLEADO, EL CUAL PEDIRA LOS DATOS, Y SE GENERA UNA USERNAME Y UNA CONTRASENA MEDIANTE UNA FUNCION
        """
        if command == '1':
            clear_screen()
            print(sep)
            cprint("\t\t\tRegistro de empleado")
            print(sep)
            while True:
                actualizar_workers_csv()
                print(f"\nIngrese el documento de identificacion, nombre, apellido, sexo {colored('(M para Masculino y F para Femenino)', 'yellow')}, edad y numero de celular, separados por comas, o ingresa \'{colored('back', 'light_blue', 'on_black')}\'\npara regresar al menu principal: ")
                command = input()
                if command == 'back':
                    break
                try:
                    id, name, last_name, second_lastname, sex, age, cel_number = command.split(",")
                    password = password_worker(name)
                    registrar_Empleado(int(id), name.capitalize(), last_name.capitalize(), second_lastname.capitalize(), sex, int(age), int(cel_number), password)
                    clear_screen()
                except:
                    cprint("\nERROR AL REGISTRAR EL USAURIO, INGRESA TODOS LOS DATOS", 'red')

            # REGISTRAR PRODUCTO

        elif command == '2':
            while True:
                print(f"Ingrese el nombre del producto, su precio y cuantas cantidades existen, si deseas devolver al\nmenu principal ingrese el comando \'{colored('back', 'light_blue', 'on_black')}\'")
                command = input().upper()
                if command == "BACK":
                    break
                else:
                    try:
                        name_product, price, quantity = command.split()
                        product = registrar_producto(name_product.capitalize(), int(price), int(quantity))
                        if product:
                            cprint("Producto ha sido registrado correctamente", "green")
                            time.sleep(2)
                            break
                        else:
                            cprint("Producto ya existe", "red")
                            time.sleep(2)
                    except:
                        cprint("Ingresa bien los valores", "yellow")
                        time.sleep(2)



        #VERIFICAR EXISTENCIA DE PRODUCTO

        elif command == '3':
            print(f"Ingresa el nombre del producto que deseas para comprobar su existencia, si deseas devolver al\nmenu principal ingrese el comando \'{colored('back', 'light_blue', 'on_black')}\'")
            product = input().upper()
            result = existencia_producto(product)
            if isinstance(result, tuple):
                cprint(f"El producto {result[1]} con id {result[2]}, tiene un valor de {result[3]} y hay {result[4]} unidad/unidades disponibles", "magenta")
            elif product == "BACK":
                pass
            else:
                cprint(f"Producto no existe", "red")
            time.sleep(2)




        elif command == '4':

            print(products_list())
            input()


        elif command == '5':

            start_sales()

        elif command == 'HELP':

            print("Los comandos son los que se usan son los siguientes:\n\n1. Registrar Empleado\n2. Registrar Producto\n3. Buscar producto\n4. Productos en inventario\n5.Venta\n6.Reporte Ventas\n")
            cprint(sep, 'red')
            input()

        elif command == 'STOP':
            break

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    clear_screen()
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    hora_actual = datetime.datetime.now().strftime("%H:%M")

    compra_lista = {
        'id': [],
        'producto': [],
        'cantidad': [],
        'Precio Unidad': [],
        'Precio': []
    }
    user = 1076904384
    password = '279AXD'
    while True:
        clear_screen()
        total = sum(compra_lista['Precio'])
        print(f"""\n\t|{"-".center(60, "-")}|{"-".center(60, "-")}|{"-".center(60, "-")}|""")
        print(f"""\t|{colored("Fecha".center(60, "-"), "blue")}|{colored("Hora".center(60, "-"), "blue")}|{colored("ID".center(60, "-"), "blue")}|""")
        print(f"""\t|{"-".center(182, "-")}|""")
        print(f"""\t|{colored(fecha.center(60, " "), "yellow")}|{colored(hora_actual.center(60, " "), "yellow")}|{colored(str(user).center(60, " "), "yellow")}|""")
        # separador
        print(f"""\t|{"-".center(182, "-")}|\n\n""")
        print(f"""\t|{colored("ID Producto".center(25, "-"), "blue")}|{colored("Producto".center(91, "-"), "blue")}|{colored("Cantidad".center(18, "-"), "blue")}|{colored("Precio X Unidad".center(25, "-"), "blue")}|{colored("Precio".center(19, "-"), "blue")}|""")

        for id, producto, cantidad, Precio_unidad, Precio in zip(compra_lista['id'], compra_lista['producto'],
                                                                 compra_lista['cantidad'],
                                                                 compra_lista['Precio Unidad'], compra_lista['Precio']):
            print(f"\t|{str(id).center(25, ' ')}|{producto.capitalize().center(91, ' ')}|{str(cantidad).center(18, ' ')}|{str(Precio_unidad).center(25, ' ')}|{str(Precio).center(19, ' ')}|")


        product = input('\t|Ingresa Id o Nombre del producto: ').capitalize()

        # Se establecen las variables que reciben el return de la funcion existencia_producto que son True || False, id_product, name , price_product, quantity_product

        comprobacion = existencia_producto(product)

        if comprobacion:

            id_prod, info_product, price_product, quantity_product = comprobacion[1:]
            cant_product = int(input('\tCuantas unidades llevara: '))

            if cant_product <= int(quantity_product) or quantity_product == 0:
                if id_prod in compra_lista['id']:

                    #Se obtiene el index del producto ya que su precio y otros valores estaran en el mismo id que en la llave id

                    locate_producto = compra_lista['id'].index(id_prod)

                    compra_lista['cantidad'][locate_producto] = cant_product

                    compra_lista['Precio'][locate_producto] = cant_product*price_product

                    Products_csv.loc[id_prod, 'quantity'] = cantidad
                    Products_csv.to_csv('Assets/products.csv')

                    continue

                cantidad = Products_csv.loc[id_prod, 'quantity'] - int(cant_product)

                compra_lista['id'].append(id_prod)
                compra_lista['producto'].append(info_product)
                compra_lista['cantidad'].append(cant_product)
                compra_lista['Precio Unidad'].append(price_product)
                compra_lista['Precio'].append(int(cant_product) * price_product)


                # Se Realiza el cambio de la cantidad del producto del CSV

                Products_csv.loc[id_prod, 'quantity'] = cantidad
                Products_csv.to_csv('Assets/products.csv')

            else:
                print("\tNo hay unidades suficientes en el inventario")
                input()
                continue

        elif product == 'Terminar':
            clear_screen()
            print(f"""\n\t|{"-".center(60, "-")}|{"-".center(60, "-")}|{"-".center(60, "-")}|""")
            print(
                f"""\t|{colored("Fecha".center(60, "-"), "blue")}|{colored("Hora".center(60, "-"), "blue")}|{colored("ID".center(60, "-"), "blue")}|""")
            print(f"""\t|{"-".center(182, "-")}|""")
            print(
                f"""\t|{colored(fecha.center(60, " "), "yellow")}|{colored(hora_actual.center(60, " "), "yellow")}|{colored(str(user).center(60, " "), "yellow")}|""")
            # separador
            print(f"""\t|{"-".center(182, "-")}|\n\n""")
            print(
                f"""\t|{colored("ID Producto".center(25, "-"), "blue")}|{colored("Producto".center(91, "-"), "blue")}|{colored("Cantidad".center(18, "-"), "blue")}|{colored("Precio X Unidad".center(25, "-"), "blue")}|{colored("Precio".center(19, "-"), "blue")}|""")

            for id, producto, cantidad, Precio_unidad, Precio in zip(compra_lista['id'], compra_lista['producto'],
                                                                     compra_lista['cantidad'],
                                                                     compra_lista['Precio Unidad'],
                                                                     compra_lista['Precio']):
                print(
                    f"\t|{str(id).center(25, ' ')}|{producto.capitalize().center(91, ' ')}|{str(cantidad).center(18, ' ')}|{str(Precio_unidad).center(25, ' ')}|{str(Precio).center(19, ' ')}|")
            print(f"""\t|{"-".center(182, "-")}|""")
            print(f"""\t|{"TOTAL:".center(174, " ")}|{str(total).center(7, " ")}|""")
            valor_pago = input("Pago: ")
            if valor_pago < total:
                cprint("El pago es menor que el total de la compra", "red")
                time.sleep(2)
                continue
            time.sleep(2)
            break
        elif product == 'Eliminar':
            product = input('\tIngresa el nombre del producto que deseas eliminar: ').capitalize()
            if product in compra_lista['producto']:
                locate_producto = compra_lista['producto'].index(producto)
                #eliminar los elementos del array
                compra_lista['id'].pop(locate_producto)
                compra_lista['producto'].pop(locate_producto)
                compra_lista['cantidad'].pop(locate_producto)
                compra_lista['Precio Unidad'].pop(locate_producto)
                compra_lista['Precio'].pop(locate_producto)
                input()
            else:
                print("\tEl Producto no esta en la lista de Compra")
        elif product == 'Salir':
            cprint("\tSaliendo...", "yellow")
            time.sleep(3)
            break
        else:
            print("\tProducto No encontrado, ingrese Nuevamente los datos del producto")
            input()
            continue

    # IMPRESION DE FACTURA
    hora_actual = datetime.datetime.now().strftime("%H:%M")
    valor_pago

    borde = "-".center(182, " ")
