# Caso práctico end-to-end: extracción de datos de la API de PokéAPI, procesamiento con ETLs y despliegue interactivo en la nube con Streamlit

Trabajo de Fin de Máster del curso CIDAEN 2024/2025 (Máster de Formación Permanente en Ciencia de Datos e Ingeniería de Datos en la Nube de la UCLM).

**Autor**: Anselmo Martínez Martínez

---

## Resumen

Para este trabajo de Fin de Máster se ha desarrollado una aplicación interactiva donde se puede consultar la información más importante acerca de las criaturas de los videojuegos de Pokémon, la cual hace uso de una serie de datos que han sido extraídos directamente de una API que proporciona todo tipo de datos relacionados con Pokémon y que se han sometido a varios procesos de transformación y limpieza para adaptarlos a la aplicación. 

Contiene tres páginas:
* “Pokédex”: una recopilación de los datos más importantes acerca de cada Pokémon y sus formas (recreando la Pokédex existente dentro de los videojuegos). Se ha creado con la intención de que sea una wiki en la que poder consultar cualquier dato del Pokémon elegido e incluso que proporcione más información de la que suelen mostrar normalmente los propios videojuegos.
* “Filters”: una serie de filtros que se pueden activar o desactivar para realizar consultas a los conjuntos de datos que hemos preparado. Se ha creado con la intención de que cualquier persona pueda hacer consultas y pueda ver los datos de las filas seleccionadas de una manera sencilla sin necesidad de tener conocimientos informáticos sobre lenguajes de consultas.
* “Minigame”: un pequeño juego de adivinar el nombre de un Pokémon específico a partir de una serie de pistas sobre sus datos. Se ha creado con la intención de poner en práctica los conocimientos adquiridos a partir de observar los datos de cada Pokémon y ofrecer un pasatiempo divertido.

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
