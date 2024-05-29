import streamlit as st
import requests
import time
import pandas as pd
import altair as alt
from PIL import Image, ImageDraw, ImageFont

#base_url = "https://mojarras-server.vercel.app"
#endpoint = "/api/traffic"
#url = base_url + endpoint

#url = "http://172.20.10.8:8081/crud/traffic/last"
url= "http://localhost:8081/crud/traffic/last"

def obtener_datos_trafico(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_json = response.json()

        print(data_json)
    
        return data_json

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Other error occurred: {err}')
    except ValueError as json_err:
        print(f'JSON parse error: {json_err}')
    
    return None

def mostrar_informacion_trafico():
    datos = obtener_datos_trafico(url)
    if datos:
        timer = datos.get("timer", 0)
        cars = datos.get("cars", [])
        st.write("### Timer ⏲️:")
        st.write(f"{timer} segundos")
        
        st.write("### Número de carros por semáforo 🚗:")
        
        
        df = pd.DataFrame({
            'Semáforo': [f"Semáforo {i + 1}" for i in range(len(cars))],
            'Número de carros': cars
        })
        
        
        chart = alt.Chart(df).mark_bar().encode(
            x='Semáforo',
            y='Número de carros',
            color='Semáforo'
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        
        for i, num_cars in enumerate(cars):
            st.write(f"*Semáforo {i + 1}*: {num_cars} carros")

        time.sleep(2)
            
        st.experimental_rerun()
    else:
        st.warning("No se pudo obtener datos del servidor.")
        
def abrir_imagen_con_transparencia(path, size):
    imagen = Image.open(path)
    if imagen.mode != 'RGBA':
        imagen = imagen.convert('RGBA')
    # Redimensionar la imagen
    imagen = imagen.resize(size, Image.ANTIALIAS)
    return imagen

def mostrar_control_semaforos():
    
    # Cargar la imagen base
    base_image_path = r"C:\Users\wgons\Downloads\bayern\calle.jpeg"
    base_image = Image.open(base_image_path)

    # Tamaño de las imágenes de los semáforos
    semaforo_size = (50, 50)  # Ajusta el tamaño según tus necesidades

    # Rutas de las imágenes de los semáforos
    semaforo_verde_path = r"C:\Users\wgons\Downloads\bayern\verde2.png"
    semaforo_rojo_path = r"C:\Users\wgons\Downloads\bayern\rojo2.png"
    semaforo_verde = abrir_imagen_con_transparencia(semaforo_verde_path, semaforo_size)
    semaforo_rojo = abrir_imagen_con_transparencia(semaforo_rojo_path, semaforo_size)

    # Posiciones de los semáforos en la imagen base
    semaforo_positions = [(600, 380), (380, 400), (490, 600), (480, 200)]

    while True:
        datos = obtener_datos_trafico(url)
        if datos:
            traffic_light = datos.get("trafficLight", 0)
            semaforos = ["Semáforo 1", "Semáforo 2", "Semáforo 3", "Semáforo 4"]

            # Crear una copia de la imagen base
            image_with_semaforos = base_image.copy()

            # Superponer las imágenes de los semáforos
            for i, pos in enumerate(semaforo_positions, start=1):
                if i == traffic_light:
                    image_with_semaforos.paste(semaforo_verde, pos, semaforo_verde)
                else:
                    image_with_semaforos.paste(semaforo_rojo, pos, semaforo_rojo)

            # Mostrar la imagen en Streamlit
            st.image(image_with_semaforos, use_column_width=True)

            # Esperar 5 segundos antes de actualizar
            time.sleep(5)
            st.experimental_rerun()
        else:
            st.warning("No se pudo obtener datos del servidor.")
            time.sleep(5)
            st.experimental_rerun()



pagina = st.sidebar.radio("Selecciona una página", ["Información de Tráfico", "Control de Semáforos"])

if pagina == "Información de Tráfico":
    st.header("Información de Tráfico")
    mostrar_informacion_trafico()

elif pagina == "Control de Semáforos":
    st.header("Control de Semáforos")
    mostrar_control_semaforos()