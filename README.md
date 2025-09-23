# Caso práctico end-to-end: extracción de datos de la API de PokéAPI, procesamiento con ETLs y despliegue interactivo en la nube con Streamlit

Trabajo de Fin de Máster del curso CIDAEN 2024/2025 (Máster de Formación Permanente en Ciencia de Datos e Ingeniería de Datos en la Nube de la UCLM).

**Autor**: Anselmo Martínez Martínez

---

## Resumen

Para este trabajo de Fin de Máster se ha desarrollado una aplicación interactiva donde se puede consultar la información más importante acerca de las criaturas de los videojuegos de Pokémon, la cual hace uso de una serie de datos que han sido extraídos directamente de una API que proporciona todo tipo de datos relacionados con estas criaturas y que se han sometido a varios procesos de transformación y limpieza para adaptarlos a la aplicación. 

Contiene tres páginas:
* “Pokédex”: una recopilación de los datos más importantes acerca de cada Pokémon y sus formas (recreando la Pokédex existente dentro de los videojuegos). Se ha creado con la intención de que sea una wiki en la que poder consultar cualquier dato del Pokémon elegido e incluso que proporcione más información de la que suelen mostrar normalmente los propios videojuegos.
* “Filters”: una serie de filtros que se pueden activar o desactivar para realizar consultas a los conjuntos de datos que hemos preparado. Se ha creado con la intención de que cualquier persona pueda hacer consultas y pueda ver los datos de las filas seleccionadas de una manera sencilla sin necesidad de tener conocimientos informáticos sobre lenguajes de consultas.
* “Minigame”: un pequeño juego de adivinar el nombre de un Pokémon específico a partir de una serie de pistas sobre sus datos. Se ha creado con la intención de poner en práctica los conocimientos adquiridos a partir de observar los datos de cada Pokémon y ofrecer un pasatiempo divertido.

---

## Desarrollo

Se ha desarrollado una aplicación interactiva desplegada en la nube con Streamlit a partir de varios procesos ETL siguiendo una arquitectura Medallion, los cuales consisten en: la extracción de varios conjuntos de datos de una API, procesos de limpieza de los datos (transformaciones, arreglo de errores, combinaciones, etc) y finalmente la carga de los datos procesados en el servicio de almacenamiento de S3 en Amazon Web Services (AWS), de donde la aplicación los recoge y los muestra en su propia interfaz.

<img width="1172" height="660" alt="esquema" src="https://github.com/user-attachments/assets/9bd1a322-8fc4-4fb5-94c8-eefd45869e23" />

---

## Acceder a la aplicación desplegada en la nube

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
