import requests 
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
from datetime import datetime 

def obtener_datos():
    # Obtiene los valores seleccionados por el usuario en el menu
    tipo_evento = evento_var.get()
    
    # Obteniene las magnitudes mínima y máxima ingresadas por el usuario
    magnitud_min = magnitud_min_var.get()
    magnitud_max = magnitud_max_var.get()

    # URL de la api con los parámetros seleccionados
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventtype={tipo_evento}&starttime=2014-01-01&endtime=2014-01-02"
    
    # Añadir magnitudes mínima y máxima a la URL si existem
    if magnitud_min:
        url += f"&minmagnitude={magnitud_min}"
    if magnitud_max:
        url += f"&maxmagnitude={magnitud_max}"

    print("URL de consulta:", url)  
    response = requests.get(url) #Realiza la solicitud a la api
    
    # se verifica si se hiz bien la solicitud
    if response.status_code == 200:
        datos = response.json() # obetiene los datos en json
        mostrar_datos(datos) # muestra los datos en la interfaz
    else:
        texto_resultado.insert(tk.END, f"Error al obtener los datos. Código de estado: {response.status_code}\n")

def mostrar_datos(datos):
    texto_resultado.delete(1.0, tk.END)  # Limpiar el área de texto
    if not datos['features']:  # Verificar si features está vacío
        texto_resultado.insert(tk.END, "No hay resultados acerca de esta consulta. Puede generar otra consulta si lo desea.\n")
        return  # Salir de la función si no hay datos
    
    # Encabezados de la tabla
    encabezados = f"{'Magnitud':<15} | {'Lugar':<70} | {'  Tiempo':<30}\n"
    texto_resultado.insert(tk.END, encabezados)
    texto_resultado.insert(tk.END, '-' * len(encabezados) + '\n')  # Línea de separación

    # Buscar en cada evento
    for evento in datos['features']:
        magnitud = evento['properties']['mag']
        lugar = evento['properties']['place']
        tiempo = evento['properties']['time']
        
        # Convierte el tiempo a un formato legible
        tiempo_legible = convertir_tiempo(tiempo)

        # Mostrar los datos en formato de tabla
        texto_resultado.insert(tk.END, f"{magnitud:<19}  {lugar:<65}  {tiempo_legible:<30}\n")
        texto_resultado.insert(tk.END, '-' * len(encabezados) + '\n')  # Línea de separación

def convertir_tiempo(tiempo_ms):
    return datetime.fromtimestamp(tiempo_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Datos de Terremotos")

# Para la ventana de la intefaz
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
ancho_ventana = int(ancho_pantalla * 0.75)  # Tamaño del 75% de ancho de la pantalla
alto_ventana = int(alto_pantalla * 0.75)  # Tamaño del 75% de alto de la pantalla
pos_x = (ancho_pantalla - ancho_ventana) // 2
pos_y = (alto_pantalla - alto_ventana) // 2
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

# Color del fondo de la interfaz
ventana.configure(bg='lightblue')

# Establecer la fuente redondeada (Arial Rounded)
rounded_font = font.Font(family='Arial Rounded', size=12)

# Título
titulo = tk.Label(ventana, text="Datos de Terremotos", font=(rounded_font, 16, 'bold'), bg='lightblue')
titulo.pack(pady=10)  # padding

# Menú desplegable para tipo de evento
evento_var = tk.StringVar(value="earthquake")  # Valor por defecto
evento_label = tk.Label(ventana, text="Seleccione un tipo de evento:", font=rounded_font, bg='lightblue')
evento_label.pack(pady=5)

evento_menu = tk.OptionMenu(ventana, evento_var, "earthquake", "explosion")  # Tipos de eventos 
evento_menu.pack(pady=5)

# Entrada para magnitud mínima
magnitud_min_label = tk.Label(ventana, text="Ingrese magnitud mínima:", font=rounded_font, bg='lightblue')
magnitud_min_label.pack(pady=5)

magnitud_min_var = tk.StringVar()  # Variable para capturar el valor ingresado
magnitud_min_entry = tk.Entry(ventana, textvariable=magnitud_min_var, font=rounded_font)
magnitud_min_entry.pack(pady=5)

# Entrada para magnitud máxima
magnitud_max_label = tk.Label(ventana, text="Ingrese magnitud máxima:", font=rounded_font, bg='lightblue')
magnitud_max_label.pack(pady=5)

magnitud_max_var = tk.StringVar()  # Variable para capturar el valor ingresado
magnitud_max_entry = tk.Entry(ventana, textvariable=magnitud_max_var, font=rounded_font)
magnitud_max_entry.pack(pady=5)

# area de texto para mostrar resultados 
texto_resultado = scrolledtext.ScrolledText(ventana, width=80, height=15, bg='lightyellow', fg='black', font=rounded_font)
texto_resultado.pack(padx=10, pady=(5, 20))  # Añadir márgenes, más espacio abajo

# Boton para consultar
boton_obtener = tk.Button(ventana, text="Consultar", command=obtener_datos, bg='white', font=rounded_font)
boton_obtener.pack(pady=10)  # Mover el botón a la parte inferior

# Ejecutar la aplicación
ventana.mainloop()
