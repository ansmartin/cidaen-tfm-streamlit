# Caso práctico end-to-end: extracción de datos de la API de PokéAPI, procesamiento con ETLs y despliegue interactivo en la nube con Streamlit

Trabajo de Fin de Máster del curso CIDAEN 2024/2025 (Máster de Formación Permanente en Ciencia de Datos e Ingeniería de Datos en la Nube de la UCLM).

**Autor**: Anselmo Martínez Martínez

---

## Resumen

Para este trabajo de Fin de Máster se ha desarrollado una aplicación interactiva desplegada en la nube donde poder consultar los datos más importantes acerca de todas las criaturas de los videojuegos de Pokémon.

Contiene tres páginas:
* “Pokédex”: una recopilación de los datos más importantes acerca de cada Pokémon y sus formas (recreando la Pokédex existente dentro de los videojuegos). Se ha creado con la intención de que sea una wiki en la que poder consultar cualquier dato del Pokémon elegido e incluso que proporcione más información de la que suelen mostrar normalmente los propios videojuegos.
* “Filters”: una serie de filtros que se pueden activar o desactivar para realizar consultas a los conjuntos de datos que hemos preparado. Se ha creado con la intención de que cualquier persona pueda hacer consultas y pueda ver los datos de las filas seleccionadas de una manera sencilla sin necesidad de tener conocimientos informáticos sobre lenguajes de consultas.
* “Minigame”: un pequeño juego de adivinar el nombre de un Pokémon específico a partir de una serie de pistas sobre sus datos. Se ha creado con la intención de poner en práctica los conocimientos adquiridos a partir de observar los datos de cada Pokémon y ofrecer un pasatiempo divertido.

Toda esta información ha sido extraída directamente de una API de datos de Pokémon (la API de PokéAPI) y se ha sometido a varios procesos de limpieza como transformaciones, arreglo de errores, combinaciones, etc.

---

## Desarrollo

En la siguiente figura podemos ver un diagrama general del flujo que siguen los datos.

<img width="1172" height="660" alt="esquema" src="https://github.com/user-attachments/assets/9bd1a322-8fc4-4fb5-94c8-eefd45869e23" />

Primero se extraen de la API con una ETL sencilla que descarga y guarda los datos en el servicio de almacenamiento de S3 en Amazon Web Services (AWS). 

A continuación estos datos siguen un proceso de mejora gracias a la arquitectura Medallion, la cual consiste en un diseño de calidad de datos utilizado para mejorar los datos de manera incremental mediante el uso de tres capas diferentes por las que van pasando: Bronze (bronce), Silver (plata) y Gold (oro):
* Bronze: Los datos de la capa bronce consisten en una copia de los datos en crudo lo más cercanos posible al origen del que proceden pero dotados de un esquema y sin realizarles modificaciones de ningún tipo ya que el propósito de esta capa es proveer un archivo histórico de los datos originales. De esta forma si fuera necesario volver a procesar los datos de capas siguientes entonces no sería obligatorio tener que leer de nuevo los datos desde el sistema original porque ya los tenemos aquí guardados. Gracias a ésto podemos recrear cualquier estado que hayan tenido los datos en cualquier momento.
* Silver: En esta capa se llevan a cabo transformaciones para limpiar y enriquecer los datos, ya sea mediante eliminar errores o inconsistencias, renombrar variables, creación de nuevas variables a partir de la lógica de negocio, unir tablas, etc. Sin embargo, nunca se realizarán agregaciones en esta capa ya que destruyen información útil que no podrá pasar a la siguiente capa.
* Gold: En esta capa se realizan filtrados y agregaciones para adaptar los datos a la aplicación.

Los resultados de cada capa se van guardando en una carpeta diferente de S3 en AWS con el mismo nombre de la capa. 

Finalmente la aplicación cada vez que se ejecuta manda una petición inicial a AWS para leer los datos de la capa Gold y así poder mostrarlos en su interfaz. Ésta se ha desarrollado gracias a la librería de Streamlit, la cual permite crear aplicaciones interactivas de manera rápida y sencilla además de poder desplegarlas en la nube gracias a su plataforma web llamada Streamlit Community Cloud.

---

## Acceder a la aplicación en la nube

La aplicación se encuentra desplegada en los servidores de la plataforma de Streamlit Community Cloud, donde puede ser accedida mediante el siguiente enlace: https://cidaen-tfm-pokeapi-app.streamlit.app/

---

## Cómo iniciar la aplicación en tu propia máquina

1. Instalar las dependencias incluidas en el fichero requirements:

   ```
   $ pip install -r requirements.txt
   ```

2. Iniciar el archivo principal de la aplicación con Streamlit:

   ```
   $ streamlit run Main.py
   ```

---

## Imagen de la aplicación

<img width="1501" height="874" alt="paginapokedex0" src="https://github.com/user-attachments/assets/5074ce6a-5297-43ef-be0b-0c5185689600" />
