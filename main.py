import time
import pandas as pd
import random
from termcolor import colored, cprint

Workers_csv = pd.read_csv("Assets/workers.csv")
Products_csv = pd.read_csv("Assets/products.csv", index_col=0)

pd.options.display.max_rows = None

sep = '--------------------------------------------------------------------------'

def actualizar_workers_csv():

    # Se decide llamar la variable correspondiente al dataframe y se le asigna que se lea nuevamente en una variable,
    # permitiendo que se mantega la lectura desde su ultima modificacion y al final con la funcion concat(), se unen los
    # data frames y se genera uno solo

    global Workers_csv
    global Products_csv
    new_data = pd.read_csv('Assets/workers.csv')
    new_data_products = pd.read_csv('Assets/products.csv')
    Products_csv = pd.concat([Products_csv, new_data_products], ignore_index=True)
    Workers_csv = pd.concat([Workers_csv, new_data], ignore_index=True)

def registrar_Empleado(id, name, last_name, second_lastname,sex, age, mobile_number, username, password, selling_products=0):
    if (Workers_csv['id'] == id).any():
        return cprint(f"El siguiente empleado {name} {last_name}, ya se encuentra registrado")
    else:
        with open('Assets/workers.csv', mode='+a') as workers:
            workers.write(f"{id},{name},{last_name},{second_lastname},{sex},{age},{mobile_number},{username},{password},{selling_products}\n")
            workers.close()
        time.sleep(2)
        output = cprint("Empleado Registrado Correctamente", "green")

    return output


def registrar_producto(name_product, price, quantity):

    with open('Assets/products.csv', mode = 'a+') as products:
        products.write(f"\n{name_product},{price},{quantity}")
    products.close()
    return
def existencia_producto(name_product):

    """
    Al tener definido como columna de index name_product de products.csv, se usa loc para facilitar encontrar
    el valor de lo que se pide, dataframe.loc[index, columna]
    """
    try:
        price_product = Products_csv.loc[f"{name_product}", "price"]
        quantity_product = Products_csv.loc[f"{name_product}", "quantity"]
        return f"El producto {name_product}, tiene un valor de {price_product} y hay {quantity_product} unidad/unidades disponibles "

    except:
        return "No existe el producto"

def products_list():
    print(Products_csv)

def username_and_password(name, last_name):
    password = str(random.randint(111, 999)) + name[::3]
    if len(name.split()) > 1:
        first_name, second_name = name.split()
        user = first_name[0:3]+second_name[0:2]+'_'+last_name[::3]
        return user, password
    user = name[0:3]+'_'+last_name[0:4]
    return user, password




def main():
    cprint("------------------------------GESTOR VENTAS----------------------------\n", 'yellow')
    while True:

        command = input(f"Ingresa un comando, en caso de no conocer un comando ingrese \'{colored('help', 'green', 'on_dark_grey')}\': ").upper()


        """
        OPCION DE REGISTRO DE EMPLEADO, EL CUAL PEDIRA LOS DATOS, Y SE GENERA UNA USERNAME Y UNA CONTRASENA MEDIANTE UNA FUNCION
        """
        if command == '1':
            print(sep)
            cprint("\n-----------------Registro de empleado-----------------------\n")
            while True:
                actualizar_workers_csv()
                print(f"Ingrese el documento de identificacion, nombre, apellido, sexo {colored('(M para Masculino y F para Femenino)', 'yellow')}, edad y numero de celular, separados por comas, o ingresa \'{colored('back', 'light_blue', 'on_black')}\'\npara regresar al menu principal: ")
                command = input()
                if command == 'back':
                    break
                try:
                    id, name, last_name, second_lastname, sex, age, cel_number = command.split(",")
                    username, password = username_and_password(name, last_name)
                    registrar_Empleado(int(id), name, last_name, second_lastname, sex, age, cel_number, username, password)

                except:
                    cprint("\nERROR AL REGISTRAR EL USAURIO, INGRESA TODOS LOS DATOS", 'red')

            # REGISTRAR PRODUCTO

        elif command == '2':
            print(f"Ingrese el nombre del producto, su precio y cuantas cantidades existen, si deseas devolver al\nmenu principal ingrese el comando \'{colored('back', 'light_blue', 'on_black')}\'")
            name_product, price, quantity = input().split()
            registrar_producto(name_product, price, quantity)

        elif command == '3':
            pass
        elif command == '4':
            products_list()
        elif command == 'HELP':
            print("Los comandos son los que se usan son los siguientes:\n\n1. Registrar Empleado\n2. Registrar Producto\n3. Buscar producto\n4. Productos en inventario\n5.Venta\n6.Reporte Ventas\n")
            cprint(sep, 'red')
            time.sleep(2)
        elif command == 'STOP':
            break

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #main()
    print(type(Products_csv.loc['MANZANA']))