
import datetime
import os
import time
import pandas as pd
import random
import ctypes
from termcolor import colored, cprint
from fpdf import FPDF
import getpass
import warnings
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# DETECTANDO DECLARACION DE PERMISOS DE ADMINISTRADOR EN WINDWOS

def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False
if os.name == 'nt':
    if es_admin():
        pass
    else:
        warnings.warn("INICIA EL PROGRAMA CON PERMISOS DE ADMINISTRADOR", UserWarning)
        exit()





Workers_csv = pd.read_csv("Assets/workers.csv")
Products_csv = pd.read_csv("Assets/products.csv", index_col=0)

pd.options.display.max_rows = None


menu = """
1. Registrar Empleado
2. Registrar Producto
3. Verificar existencia de un producto
4. Productos en el inventario
5. Iniciar Venta
6. Productos por agotarse
"""

sep = '--------------------------------------------------------------------------'

os.environ["TERM"] = "xterm"

#exit()
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
def registrar_Empleado(id, name, last_name, second_lastname, sex, age, mobile_number, password, selling_products=0):
    if (Workers_csv['id'] == id).any():
        return cprint(f"El siguiente empleado {name} {last_name}, ya se encuentra registrado\n")
    else:
        with open('Assets/workers.csv', mode='+a') as workers:
            workers.write(
                f"{id},{name},{last_name},{second_lastname},{sex},{age},{mobile_number},{password},{selling_products}\n")
            workers.close()
        time.sleep(2)
        output = cprint(
            f"El Empleado con {id} ha sido Registrado Correctamente.\nLa contraseña para el inicio de caja es: {password}\n",
            "green")

    return output


# command = 2
def registrar_producto(name_product, price, quantity):
    id_product = Products_csv.index[-1] + 1

    existencia = existencia_producto(name_product)

    if isinstance(existencia, tuple):
        return False
    else:

        with open('Assets/products.csv', mode='a+') as products:
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
            return True, id_product, name, price_product, quantity_product
        else:
            return False


# command = 4
def products_list():
    return f"\n{Products_csv}\n"


# --------------- FUNCION PARA ENVIAR AL CORREO --------------------------
def send_checkout(ruta,documento,correo):
    mensaje = MIMEMultipart("plain")
    mensaje["From"] = "projectarek@outlook.com"
    mensaje["To"] = correo
    mensaje["Subject"] = "ENTREGA DE FACTURA"
    factura = MIMEApplication(open(f"{ruta}/{documento}", "rb").read())
    factura.add_header("Content-Disposition", 'attachment', filename=documento)
    mensaje.attach(factura)
    smtp = SMTP("smtp-mail.outlook.com", 587)
    smtp.starttls()
    smtp.login("projectarek@outlook.com", "qazedcwsxtgbrfv575")
    smtp.sendmail("projectarek@outlook.com", correo, mensaje.as_string())
    smtp.quit()
    return  "Factura generada y enviada exitosamente."

# --------------------------------------------------------------------------------


# ----------------------------- GENERACION PDF------------------------------------

def checkout_pdf(seller_id, fecha_today, hora_check, list_products, total, correo):

    warnings.filterwarnings("ignore")

    #------VARIABLE TEXTO-----------



    text_footer = f"La factura generada se ha enviado al correo asignado  {correo}\n" \
                  "Github: https://github.com/Arekkasu    |" \
                  "    Correo dev: alexanderlozada230@gmail.com"

    directorio = os.getcwd()

    usuario_dispositivo = getpass.getuser()

    facturas_carpeta = f"{directorio}/facturas"

    fechas_facturas = f"{facturas_carpeta}/{fecha_today}"

    nuevo_documento = f"Factura_{fecha_today}_{hora_check}.pdf"
    """Estableciendo los permisos para que se pueda escribir en la carpeta"""

    if os.name == 'posix': # en caso que sea linux
        os.chmod(directorio, 0o700)
    elif os.name == 'nt':
        comando = f'icacls "{directorio}" /grant:r {usuario_dispositivo}:(OI)(CI)F'
        os.system(comando)
    #-------------------------------

    #---GENERACION DE PDF-----------

    pdf = FPDF()
    pdf.set_font("Arial", "", 8)
    pdf.add_page()

    #------------------------------


    #HACER TRAZOS
    pdf.set_line_width(0.2)
    pdf.set_line_width(0.25)
    #ENCABEZADO
    pdf.cell(w=5, h=10, txt='', border=0, align = 'c')
    pdf.cell(w=60, h=10, txt='FECHA', border=1, align = 'c')
    pdf.cell(w=80, h=10, txt='HORA', border=1, align = 'c')
    pdf.multi_cell(w=40, h=10, txt='ID VENDEDOR', border=1, align = 'c', ln=1)

    pdf.cell(w=5, h=10, txt='', border=0, align = 'c')
    pdf.cell(w=60, h=10, txt=fecha_today, border=1, align = 'c')
    pdf.cell(w=80, h=10, txt=hora_check, border=1, align = 'c')
    pdf.multi_cell(w=40, h=10, txt=str(seller_id), border=1, align = 'c', ln=1)

    pdf.multi_cell(w=0, h=10, txt='', border=0, align = 'c', ln=1)
    pdf.multi_cell(w=0, h=10, txt='', border=0, align = 'c', ln=1)


    #-------------- GENERACION DE FACTURA -------------

    pdf.cell(w=5, h=10, txt='', border=0, align = 'c')
    pdf.cell(w=30, h=10, txt='ID PRODUCTO', border=1, align = 'c')
    pdf.cell(w=60, h=10, txt='PRODUCTO', border=1, align = 'c')
    pdf.cell(w=30, h=10, txt='CANTIDAD', border=1, align = 'c')
    pdf.cell(w=30, h=10, txt='PRECIO x UNIDAD', border=1, align = 'c')
    pdf.multi_cell(w=30, h=10, txt='PRECIO', border=1, align = 'c', ln=1)
    product_display = 0
    for id, producto, cantidad, Precio_unidad, Precio in zip(list_products['id'],
                                                             list_products['producto'],
                                                             list_products['cantidad'],
                                                             list_products['Precio Unidad'],
                                                             list_products['Precio']):
        pdf.cell(w=5, h=10, txt='', border=0, align='c')
        pdf.cell(w=30, h=10, txt=str(id), border='B', align='c')
        pdf.cell(w=60, h=10, txt=str(producto), border='B', align='c')
        pdf.cell(w=30, h=10, txt=str(cantidad), border='B', align='c')
        pdf.cell(w=30, h=10, txt=str(Precio_unidad), border='B', align='c')
        pdf.multi_cell(w=30, h=10, txt=str(Precio), border='B', align='c', ln=1)

    #--------------------------------------------


    #----------------TOTAL DE LA COMPRA------------------


    pdf.cell(w=5, h=10, txt='', border=0, align='c')
    pdf.cell(w=30, h=10, txt='TOTAL:', border='LB', align = 'c',)
    pdf.cell(w=120, h=10, txt='', border='B', align = 'c')
    pdf.multi_cell(w=30, h=10, txt=str(total), border='RB', align = 'c', ln=1)

    #--------------------------------------------------

    # FOOTER DEL PDF DONDE ESTARA MI CONTACTO
    pdf.multi_cell(w=0, h=10, txt='', border=0, align = 'c', ln=1)
    pdf.multi_cell(w=0, h=10, txt='', border=0, align = 'c', ln=1)
    pdf.multi_cell(w=0, h=10, txt='', border=0, align = 'c', ln=1)
    pdf.set_font("Arial", "", 5)
    pdf.cell(w=5, h=10, txt='', border=0, align='c')
    pdf.multi_cell(w=0, h=10, txt=text_footer, border="T", align='c',
                   link="https://github.com/Arekkasu/Gestor-de-Negocios.git")


    #print(facturas_carpeta)
    if not os.path.exists(facturas_carpeta):
        # Crear la carpeta
        os.makedirs(facturas_carpeta)

    if not fecha_today in os.listdir(facturas_carpeta):
        os.makedirs(fechas_facturas)
        pdf.output(f"{fechas_facturas}/{nuevo_documento}")
    else:
        if nuevo_documento in os.listdir(fechas_facturas):
            contador = 1
            while nuevo_documento in os.listdir(fechas_facturas):
                nuevo_documento = f"Factura_{fecha_today}_{hora_check}_{contador}.pdf"
                contador += 1
            pdf.output(f"{fechas_facturas}/{nuevo_documento}")
        else:
            pdf.output(f"{fechas_facturas}/{nuevo_documento}")


    if os.name == "posix":
        # En Linux, utiliza xdg-open
        os.system(f"xdg-open {fechas_facturas}/{nuevo_documento}")
    elif os.name == "nt":
        # En Windows, permite al usuario seleccionar el programa
        os.startfile(f"{fechas_facturas}/{nuevo_documento}")

    send_email = send_checkout(fechas_facturas, nuevo_documento, correo)
    warnings.filterwarnings("default")
    return send_email



# -------------------------------------------------------------------------------------









# --------------------- INICIA PROCESO DE VENTA ---------------------

def start_sales():
    clear_screen()
    """
    Variables del display de la facturacion
    de la lista de compra 
    """
    fecha = datetime.date.today().strftime("%d-%m-%Y")

    hora_actual = datetime.datetime.now().strftime("%H:%M")


    # Variable de estado para saber si puede hacer factura o no

    compra_lista = {
        'id': [],
        'producto': [],
        'cantidad': [],
        'Precio Unidad': [],
        'Precio': []
    }
    while True:
        print(sep)
        print(
            f"Iniciando proceso de ventas. \nPor favor, ingrese tu {colored(f'usuario', 'green')} y tu {colored(f'contraseña', 'blue')}.")
        print(sep)
        try:
            user = int(input(f"Ingrese el numero de Identificacion: "))
        except:
            cprint("Error: El formato ingresado es incorrecto. Por favor, ingrese de manera correcta los datos.", "red")
            continue
        password = str(input(f"Ingrese la contraseña: "))
        if (Workers_csv['id'] == user).any() & (Workers_csv['password'] == password).any():
            clear_screen()
            while True:
                clear_screen()
                total = sum(compra_lista['Precio'])
                print(f"""\n|{"-".center(60, "-")}|{"-".center(60, "-")}|{"-".center(60, "-")}|""")
                print(
                    f"""|{colored("Fecha".center(60, "-"), "blue")}|{colored("Hora".center(60, "-"), "blue")}|{colored("ID".center(60, "-"), "blue")}|""")
                print(f"""|{"-".center(182, "-")}|""")
                print(
                    f"""|{colored(fecha.center(60, " "), "yellow")}|{colored(hora_actual.center(60, " "), "yellow")}|{colored(str(user).center(60, " "), "yellow")}|""")
                # separador
                print(f"""|{"-".center(182, "-")}|\n\n""")
                print(
                    f"""|{colored("ID Producto".center(25, "-"), "blue")}|{colored("Producto".center(91, "-"), "blue")}|{colored("Cantidad".center(18, "-"), "blue")}|{colored("Precio X Unidad".center(25, "-"), "blue")}|{colored("Precio".center(19, "-"), "blue")}|""")

                for id, producto, cantidad, Precio_unidad, Precio in zip(compra_lista['id'], compra_lista['producto'],
                                                                         compra_lista['cantidad'],
                                                                         compra_lista['Precio Unidad'],
                                                                         compra_lista['Precio']):
                    print(
                        f"|{str(id).center(25, ' ')}|{producto.capitalize().center(91, ' ')}|{str(cantidad).center(18, ' ')}|{str(Precio_unidad).center(25, ' ')}|{str(Precio).center(19, ' ')}|")

                product = input('|Ingresa Id o Nombre del producto: ').capitalize()

                # Se establecen las variables que reciben el return de la funcion existencia_producto que son True || False, id_product, name , price_product, quantity_product

                comprobacion = existencia_producto(product)


                # ---------SELECCIONANDO PRODUCTO -----------------
                if comprobacion:

                    id_prod, info_product, price_product, quantity_product = comprobacion[1:]
                    try:
                        cant_product = int(input('Cuantas unidades llevara: '))
                    except:
                        cprint('El valor ingresado debe ser un numero entero','red')
                        input("Presiona enter para continuar")
                        continue

                    # Condicional para asegurar la cantidad seleccionada en el inventario

                    if cant_product <= int(quantity_product):
                        if id_prod in compra_lista['id']:

                            # Se obtiene el index del producto ya que su precio y otros valores estaran en el \
                            # mismo id que en la llave id

                            locate_producto = compra_lista['id'].index(id_prod)

                            # Se obtiene el valor   de cantidad que esta registrado en la lista de compra

                            old_cant = compra_lista['cantidad'][locate_producto]

                            """
                            La siguiente condicion sucede para que en caso que se registre el mismo producto este
                            no se agrege denuevo en la lista de sino que simplemente se modifique su valor.
                            """

                            if cant_product < old_cant:
                                Products_csv.loc[id_prod, 'quantity'] = quantity_product + cant_product
                            else:
                                diferencia = cant_product - old_cant
                                Products_csv.loc[id_prod, 'quantity'] = quantity_product - diferencia

                            compra_lista['Precio'][locate_producto] = cant_product * price_product
                            compra_lista['cantidad'][locate_producto] = cant_product
                            Products_csv.to_csv('Assets/products.csv')

                            continue

                        # La cantidad que se le restara al CSV de Productos de la seccion 'quantity'

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

                        print("No hay unidades suficientes en el inventario")
                        input()
                        continue

                #--------------------------------------------------------------------------------


                # ---------------------------- HACER CHECKOUT  ------------------------------------------
                elif product == 'Terminar':

                    # Condicion que para en caso de solicitar terminar
                    # y no haya algun producto en lista, no lo permita hacer y no haya error

                    if len(compra_lista['id']) == 0:
                        cprint("|No se puede terminar la compra, no hay productos que pagar", "red")
                        time.sleep(3)
                        continue

                    clear_screen()
                    print(f"""\n|{"-".center(60, "-")}|{"-".center(60, "-")}|{"-".center(60, "-")}|""")
                    print(
                        f"""|{colored("Fecha".center(60, "-"), "blue")}|{colored("Hora".center(60, "-"), "blue")}|{colored("ID".center(60, "-"), "blue")}|""")
                    print(f"""|{"-".center(182, "-")}|""")
                    print(
                        f"""|{colored(fecha.center(60, " "), "yellow")}|{colored(hora_actual.center(60, " "), "yellow")}|{colored(str(user).center(60, " "), "yellow")}|""")
                    # separador
                    print(f"""|{"-".center(182, "-")}|\n\n""")
                    print(
                        f"""|{colored("ID Producto".center(25, "-"), "blue")}|{colored("Producto".center(91, "-"), "blue")}|{colored("Cantidad".center(18, "-"), "blue")}|{colored("Precio X Unidad".center(25, "-"), "blue")}|{colored("Precio".center(19, "-"), "blue")}|""")

                    for id, producto, cantidad, Precio_unidad, Precio in zip(compra_lista['id'],
                                                                             compra_lista['producto'],
                                                                             compra_lista['cantidad'],
                                                                             compra_lista['Precio Unidad'],
                                                                             compra_lista['Precio']):
                        print(
                            f"|{str(id).center(25, ' ')}|{producto.capitalize().center(91, ' ')}|{str(cantidad).center(18, ' ')}|{str(Precio_unidad).center(25, ' ')}|{str(Precio).center(19, ' ')}|")
                    print(f"""|{"-".center(182, "-")}|""")
                    print(f"""|{"TOTAL:".center(174, " ")}|{str(total).center(7, " ")}|""")
                    valor_pago = int(input(f"""|{"Dinero ingresado:".center(174, " ")}|"""))

                    if valor_pago < total:
                        cprint("El pago es menor que el total de la compra", "red")
                        input("preisona enter para continuar...")
                    time.sleep(1)
                    break
                #----------------------------------------------------------------------------------------------------



                # ---------------------------- ELIMINAR PRODUCTO DE LA COMPRA --------------------------------------

                elif product == 'Eliminar':
                    product = input('Ingresa el nombre del producto que deseas eliminar: ').capitalize()
                    if product in compra_lista['producto']:

                        locate_producto = compra_lista['producto'].index(producto)
                        id_producto = compra_lista['id'][locate_producto]

                        Products_csv.at[id_producto, 'quantity'] = Products_csv.at[id_producto, 'quantity'] + \
                                                                   compra_lista['cantidad'][locate_producto]

                        # Eliminacion los elementos del array

                        # Se elimina el id que estaba en el

                        compra_lista['id'].pop(locate_producto)
                        compra_lista['producto'].pop(locate_producto)
                        compra_lista['cantidad'].pop(locate_producto)
                        compra_lista['Precio Unidad'].pop(locate_producto)
                        compra_lista['Precio'].pop(locate_producto)
                        Products_csv.to_csv('Assets/products.csv')

                    else:

                        print("El Producto no esta en la lista de Compra")


                # ------------------------------ Cancelar Compra --------------------------------------------------


                elif product == 'Cancelar':
                    cprint("Saliendo...", "yellow")
                    for producto, cantidad in zip(compra_lista['id'], compra_lista['cantidad']):
                        Products_csv.at[producto, 'quantity'] = Products_csv.at[producto, 'quantity'] + \
                                                                   cantidad
                    Products_csv.to_csv('Assets/products.csv')
                    time.sleep(3)
                    return 0

                # -----------------------------------------------------------------------------------------------

                else:
                    print(" Producto No encontrado, ingrese Nuevamente los datos del producto")
                    input(" Presiona enter para continuar....")
                    continue

                #-----------------------------------------------------------------------------------------------
            """
            Impresion de factura hasta que se transporte a un archivo de pdf
            """
            clear_screen()
            hora_actual = datetime.datetime.now().strftime("%H:%M")

            print(f"""\n|{"-".center(60, "-")}|{"-".center(60, "-")}|{"-".center(60, "-")}|""")
            print(
                f"""|{colored("Fecha".center(60, "-"), "blue")}|{colored("Hora".center(60, "-"), "blue")}|{colored("ID".center(60, "-"), "blue")}|""")
            print(f"""|{"-".center(182, "-")}|""")
            print(
                f"""|{colored(fecha.center(60, " "), "yellow")}|{colored(hora_actual.center(60, " "), "yellow")}|{colored(str(user).center(60, " "), "yellow")}|""")
            # separador
            print(f"""|{"-".center(182, "-")}|\n\n""")
            print(
                f"""|{colored("ID Producto".center(25, "-"), "blue")}|{colored("Producto".center(91, "-"), "blue")}|{colored("Cantidad".center(18, "-"), "blue")}|{colored("Precio X Unidad".center(25, "-"), "blue")}|{colored("Precio".center(19, "-"), "blue")}|""")

            for id, producto, cantidad, Precio_unidad, Precio in zip(compra_lista['id'], compra_lista['producto'],
                                                                     compra_lista['cantidad'],
                                                                     compra_lista['Precio Unidad'],
                                                                     compra_lista['Precio']):
                print(
                    f"|{str(id).center(25, ' ')}|{producto.capitalize().center(91, ' ')}|{str(cantidad).center(18, ' ')}|{str(Precio_unidad).center(25, ' ')}|{str(Precio).center(19, ' ')}|")
            print(f"""|{"-".center(182, "-")}|""")
            print(f"""|{"TOTAL:".center(174, " ")}|{str(total).center(7, " ")}|""")
            print(f"""|{"-".center(182, "-")}|""")
            print(f"""|{"Dinero ingresado:".center(174, " ")}|{str(valor_pago).center(7, " ")}|""")
            print(f"""|{"-".center(182, "-")}|""")
            print(f"""|{"Cambio:".center(174, " ")}|{str(valor_pago - total).center(7, " ")}|""")
            print(f"""|{"-".center(182, "-")}|""")


            correo = input("Ingresa el correo al cual se enviara la factura: ")

            checkout_pdf(user, fecha, hora_actual, compra_lista, total, correo)

            return "Compra Finalizada"
        break


# -----------------------------------------------------------------------------------------------

# ----- FUNCION PARA SABER CUANDO SE AGOTARA UN PRODUCTO ----------------
def producto_agotarse():
    return (Products_csv['quantity'] < 50).any()




def main():
    clear_screen()
    while True:
        clear_screen()
        cprint("\n------------------------------GESTOR VENTAS----------------------------", 'yellow')



        print(menu)
        if producto_agotarse():
            print(f"{colored('productos por agotarse','yellow')}, Ingresa la opcion seis para conocer que productos son")
        command = input(f"{colored('Ingresa el numero del comando que deseas usar', 'light_grey')}: ").upper()


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
                print(
                    f"\nRegistro de empleados, si deseas salir ingresa \'{colored('back', 'light_blue', 'on_black')}\'\npara regresar al menu principal: ")
                try:
                    preguntas = [
                        "Ingresa el numero de identigicacion: ",
                        "Nombre: ",
                        "Primer Apellido: ",
                        "Segundo Apellido: ",
                        "Sexo ('M' masculino, 'F' femenino): ",
                        "Edad: ",
                        "Numero de contacto: "
                    ]

                    respuestas = []

                    for i in range(len(preguntas)):
                        pregunta = preguntas[i]
                        respuesta = input(pregunta).capitalize()

                        if respuesta == 'Back':
                            respuestas.append(respuesta)
                            break

                        elif (i == 0 or i == 5 or i == 6):
                            while not respuesta.isdigit():
                                print("El valor ingresado no es valido. Intenta nuevamente.")
                                respuesta = input(pregunta)
                        elif i == 4:
                            while not (respuesta.capitalize() == 'M' or respuesta.capitalize() == 'F'):
                                print("El valor ingresado no es valido. Intenta nuevamente.")
                                respuesta = input(pregunta)
                        respuestas.append(respuesta)

                    if 'Back' in respuestas:
                        break
                    id, name, last_name, second_lastname, sex, age, cel_number = respuestas
                    password = password_worker(name)
                    print(registrar_Empleado(int(id), name.capitalize(), last_name.capitalize(), second_lastname.capitalize(),
                                       sex, int(age), int(cel_number), password))
                    clear_screen()
                except:
                    cprint("\nERROR AL REGISTRAR EL USAURIO, INGRESA TODOS LOS DATOS", 'red')

            # REGISTRAR PRODUCTO

        elif command == '2':
            while True:
                print(
                    f"Registrar producto, si deseas devolver al\nmenu principal ingrese el comando \'{colored('back', 'light_blue', 'on_black')}\'")

                preguntas = [
                        "Ingresa el nombre del producto: ",
                        "Ingresa el precio: ",
                        "Ingresa la cantidad: ",
                    ]
                respuestas = []

                for i in range(len(preguntas)):
                    pregunta = preguntas[i]
                    respuesta = input(pregunta).capitalize()

                    if respuesta == 'Back':
                        respuestas.append(respuesta)
                        break

                    elif (i == 1 or i == 2 ):
                        while not respuesta.isdigit():
                            print("El valor ingresado no es valido. Intenta nuevamente.")
                            respuesta = input(pregunta)
                    respuestas.append(respuesta)
                print(respuestas)
                if 'Back' in respuestas:
                    break
                name_product, price, quantity = respuestas
                product = registrar_producto(name_product.capitalize(), int(price), int(quantity))
                if product:
                    cprint("Producto ha sido registrado correctamente", "green")
                    time.sleep(2)
                    break
                else:
                    cprint("Producto ya existe", "red")
                    time.sleep(2)

                cprint("Ingresa bien los valores", "yellow")
                time.sleep(2)



        # VERIFICAR EXISTENCIA DE PRODUCTO

        elif command == '3':
            print(
                f"Ingresa el nombre del producto que deseas para comprobar su existencia, si deseas devolver al\nmenu principal ingrese el comando \'{colored('back', 'light_blue', 'on_black')}\'")
            product = input().upper()
            result = existencia_producto(product)
            if isinstance(result, tuple):
                cprint(
                    f"El producto {result[1]} con id {result[2]}, tiene un valor de {result[3]} y hay {result[4]} unidad/unidades disponibles",
                    "magenta")
            elif product == "BACK":
                pass
            else:
                cprint(f"Producto no existe", "red")
            time.sleep(2)


        # HACER LISTA DE PRODUCTO

        elif command == '4':

            print(products_list())
            input("Presiona enter para continuar...")

        # INICIAR VENTA

        elif command == '5':

            print(start_sales())
            input("Presiona enter para continuar...")

        # CONOCER PRODUCTOS POR AGOTARSE
        elif command == '6':

            print("\nProductos por agotarse:\n")
            print(Products_csv.loc[Products_csv['quantity'] < 50])
            input("\nPresiona enter para continuar...")

        elif command == 'STOP':
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
