# Luis Adrian Abbarca Gomez 
# A01798043
# Evidencia 1# 

# turtle: Controla una tortuga gráfica en una ventana para crear dibujos.
# re: Procesa expresiones regulares para dividir el texto en comandos y tokens.
# tkinter: Crea una interfaz gráfica de usuario (GUI) para abrir archivos y mostrar información.
# filedialog (desde tkinter): Proporciona ventanas de diálogo para seleccionar archivos.

import turtle
import re
import tkinter as tk
from tkinter import filedialog

# Lista de colores disponibles para cambiar el color de la tortuga
colors = ["red", "blue", "green", "purple", "orange", "pink", "yellow", "brown", "black", "white", "gray", "lightblue", "lightgreen", "lightpink", "lightyellow", "gold", "cyan", "magenta", "violet", "maroon"]

# Definir la gramática BNF para analizar los comandos
Gramatica = r"""
    programa    : comando*
    comando     : cambio_color
                | limpiar_pantalla
                | movimiento
                | rotacion
                | repeticion
                | arriba_abajo
    cambio_color: "clr" color
    limpiar_pantalla: "cn"
    movimiento   : ("go" | "bk") numero
    rotacion    : ("lt" | "rt") angulo
    repeticion  : "rpt" numero
    arriba_abajo: "up" | "down"
    color       : [a-z]+
    numero      : [0-9]+ | -?[0-9]+
    angulo      : [0-9]+
"""

# Analizador sintáctico
class Parser:
    def __init__(self, text):
        self.tokens = re.findall(r'\b\w+\b', text)
        self.pos = 0

    def parse(self):
        return self.programa()

    def programa(self):
        comandos = []
        while self.pos < len(self.tokens):
            comandos.append(self.comando())
        return comandos

    def comando(self):
        token = self.tokens[self.pos]
        if token == "clr":
            self.pos += 1
            return ("clr", self.color())
        elif token == "cn":
            self.pos += 1
            return ("cn",)
        elif token in ("go", "bk"):
            movimiento = token
            self.pos += 1
            numero = self.numero()
            return (movimiento, numero)
        elif token in ("lt", "rt"):
            rotacion = token
            self.pos += 1
            angulo = self.angulo()
            return (rotacion, angulo)
        elif token == "rpt":
            self.pos += 1
            numero = self.numero()
            return ("rpt", numero)
        elif token in ("up", "down"):
            self.pos += 1
            return (token,)
        else:
            raise ValueError(f"Comando no reconocido: {token}")

    def color(self):
        token = self.tokens[self.pos]
        if token in colors:
            self.pos += 1
            return token
        else:
            raise ValueError(f"Color desconocido: {token}")

    def numero(self):
        token = self.tokens[self.pos]
        if re.match(r'^-?[0-9]+$', token):
            self.pos += 1
            return int(token)
        else:
            raise ValueError(f"Número inválido: {token}")

    def angulo(self):
        token = self.tokens[self.pos]
        if re.match(r'^[0-9]+$', token):
            self.pos += 1
            return int(token)
        else:
            raise ValueError(f"Angulo inválido: {token}")

# Función para abrir un archivo usando una ventana emergente de selección de archivo
def open_file():
    directorio_inicial = "."  # Directorio inicial (cambia esto a tu directorio deseado)
    archivo = filedialog.askopenfilename(initialdir=directorio_inicial, filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        execute_commands(archivo)

# Función para abrir un archivo manualmente
def open_manually(nombre_archivo):
    if nombre_archivo:
        execute_commands(nombre_archivo)

# Función para mostrar las reglas del lenguaje
def show_rules():
    reglas_window = tk.Toplevel() 
    reglas_window.title("Reglas")
    reglas_image = tk.PhotoImage(file="reglas.png") 
    reglas_label = tk.Label(reglas_window, image=reglas_image)
    reglas_label.image = reglas_image  
    reglas_label.pack()

# Función para mostrar los comandos disponibles
def show_commands():
    comandos_window = tk.Toplevel()  
    comandos_window.title("Comandos")
    comandos_image = tk.PhotoImage(file="comandos.png")  
    comandos_label = tk.Label(comandos_window, image=comandos_image)
    comandos_label.image = comandos_image  
    comandos_label.pack()

# Función principal para mostrar el menú interactivo
def show_menu():
    root = tk.Tk()
    root.title("Menú Interactivo")

    # Crea un Frame principal para contener todos los elementos
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20, expand=True, fill='both')

    # Crea un Canvas para mostrar la imagen de fondo
    canvas = tk.Canvas(frame, width=500, height=300)  
    canvas.grid(row=0, column=0, sticky='nsew')  

    # Carga la imagen de fondo
    fondo_image = tk.PhotoImage(file="red.png")  
    canvas.create_image(0, 0, anchor="nw", image=fondo_image)

    # Crea un Frame para los elementos del formulario
    form_frame = tk.Frame(frame, bg='#00004d', padx=10, pady=10)  
    form_frame.grid(row=1, column=0, sticky='nsew')  

    # Ajusta el texto y formato de los botones
    abrir_button = tk.Button(
        form_frame,
        text="Abrir Archivo",
        font=("Courier New", 12, "bold"),  
        command=open_file
    )
    abrir_button.grid(row=0, column=0, columnspan=2, pady=10)

    # Etiqueta para el nombre del archivo
    archivo_label = tk.Label(
        form_frame,
        text="Nombre del archivo:",
        font=("Courier New", 12, "bold")  
    )
    archivo_label.grid(row=1, column=0, padx=10, pady=5)

    # Cuadro de entrada para el nombre del archivo
    archivo_entry = tk.Entry(
        form_frame,
        font=("Courier New", 12),  
        width=30  
    )
    archivo_entry.grid(row=1, column=1, padx=10, pady=5)

    # Botón para abrir el archivo introducido manualmente
    abrir_manual_button = tk.Button(
        form_frame,
        text="Abrir Manualmente",
        font=("Courier New", 12, "bold"),  
        command=lambda: open_manually(archivo_entry.get())
    )
    abrir_manual_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Agrega el botón "Reglas"
    reglas_button = tk.Button(
        form_frame,
        text="Presiona aquí para conocer las reglas",
        font=("Courier New", 12, "bold"),
        command= show_rules
    )
    reglas_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Agregar el botón "Comandos"
    comandos_button = tk.Button(
        form_frame,
        text="Presiona aquí para conocer los comandos",
        font=("Courier New", 12, "bold"),
        command= show_commands
    )
    comandos_button.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

# Función principal para ejecutar los comandos del archivo
def execute_commands(nombre_archivo):
    turtle.speed(1)
    turtle.setup(1920, 1080)

    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()

    contenido_sin_comentarios = re.sub(r'->.*?<-', '', contenido, flags=re.DOTALL)
    comandos = contenido_sin_comentarios.split('\n')

    tortuga = turtle.Turtle()
    tortuga.penup()

    ventana_info = turtle.Screen()
    ventana_info.setup(1280, 720)
    ventana_info.title("Información del Dibujo")
    info_turtle = turtle.Turtle()
    info_turtle.penup()
    info_turtle.goto(-440, 280)
    info_turtle.pendown()
    info_turtle.write(f"Archivo: {nombre_archivo}", font=("Courier New", 15, "bold"))
    info_turtle.penup()
    info_turtle.goto(-440, 260)
    info_turtle.pendown()
    info_turtle.write("Comandos:", font=("Courier New", 14, "bold"))
    info_turtle.penup()
    info_turtle.goto(-440, 240)
    info_turtle.pendown()

    errores = []  # Lista para almacenar errores

    for num, cmd in enumerate(comandos, start=1):
        info_turtle.write(f"{num}: {cmd}", font=("Courier New", 12, "normal"))
        info_turtle.penup()
        info_turtle.goto(-440, 240 - num * 20)
        info_turtle.pendown()

        # Validar el comando y agrega errores a la lista
        error = validate_command(cmd)
        if error:
            errores.append(f"Error en la línea {num}: {error}")

    for num_linea, comando in enumerate(comandos, start=1):
        comando = comando.lower().strip()

        if not comando:
            continue

        if comando == "up":
            tortuga.penup()
            continue
        elif comando == "down":
            tortuga.pendown()
            continue

        if comando == "bg":
            go_to_center(tortuga)
            continue

        comando, repeticion = sepate_rpt_command(comando)

        error = validate_command(comando)

        if error:
            errores.append(f"Error en la línea {num_linea}: {error}")
            continue

        if re.match(r'^clr [a-z]+$', comando):
            color_nombre = comando.split()[1]
            tortuga.color(color_nombre)
        elif re.match(r'^cn$', comando):
            tortuga.clear()
        else:
            veces = int(repeticion) if repeticion else 1
            for _ in range(veces):
                detect_command(comando.strip(), tortuga)

    # Muestra los errores en la ventana de información
    info_turtle.penup()
    info_turtle.goto(-440, -300)
    info_turtle.pendown()
    for error in errores:
        info_turtle.write(error, font=("Courier New", 12, "normal"))
        info_turtle.penup()
        info_turtle.goto(-440, info_turtle.ycor() - 20)

    go_to_center(tortuga)
    show_msj("Dibujo completado")

    turtle.done()

# Función para separar el comando de la repetición (si está presente)
def sepate_rpt_command(comando):
    partes = comando.split("#")
    comando = partes[0].strip()
    repeticion = partes[1].strip() if len(partes) > 1 else None
    return comando, repeticion

# Función para validar si un comando es válido
def validate_command(comando):
    if re.match(r'^clr [a-z]+$', comando):
        color_nombre = comando.split()[1]
        if color_nombre not in colors:
            return f"Color desconocido: {color_nombre}"
    elif re.match(r'^bk -?[0-9]+$', comando):
        distancia = int(comando.split()[1])
        if distancia <= 0:
            return f"Valor inválido para retroceder: {distancia}"
    elif re.match(r'^rpt [0-9]+$', comando):
        veces = int(comando.split()[1])
        if veces <= 0:
            return f"Valor inválido para repetición: {veces}"

    return None

# Función para ejecutar un comando específico
def detect_command(comando, tortuga):
    comando = comando.lower().strip()
    if re.match(r'^go [0-9]+$', comando):
        distancia = int(comando.split()[1])
        tortuga.forward(distancia)
    elif re.match(r'^bk -?[0-9]+$', comando):
        distancia = int(comando.split()[1])
        tortuga.backward(distancia)
    elif re.match(r'^lt [0-9]+$', comando):
        angulo = int(comando.split()[1])
        tortuga.left(angulo)
    elif re.match(r'^rt [0-9]+$', comando):
        angulo = int(comando.split()[1])
        tortuga.right(angulo)

# Función para llevar la tortuga al centro de la pantalla
def go_to_center(tortuga):
    tortuga.penup()
    tortuga.goto(0, 0)
    tortuga.pendown()

# Función para mostrar un mensaje en la consola
def show_msj(mensaje):
    print(mensaje)

if __name__ == "__main__":
    show_menu()
