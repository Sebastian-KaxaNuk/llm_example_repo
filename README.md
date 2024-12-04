# LLMS_Example
Welcome to a basic openai connection example

## File Structure

Maintaining an organized folder structure is crucial to the code efficiency. Organize your files as follows:


- **`Config` Folder**: api keys.
    - `.env` file, with api keys.


## Configuración del Entorno y Dependencias

Para configurar tu entorno y asegurarte de que todas las dependencias necesarias están instaladas, sigue estos pasos:

1. **Descargar Anaconda**: Descarga la versión más reciente de Anaconda desde su [sitio web oficial](https://www.anaconda.com/products/distribution). Asegúrate de elegir la versión que corresponda a tu sistema operativo.

2. **Abrir Anaconda Prompt**: Una vez instalado Anaconda, inicia Anaconda Prompt desde tu menú de inicio.

3. **Crear un Nuevo Environment con Python 3.12**: En Anaconda Prompt, crea un nuevo environment llamado `llm_example_repo_env` con Python 3.12 utilizando el siguiente comando:
   ```bash
   conda create --name llm_example_repo_env python=3.12

4. **Activar el Environment**: Activa el environment recién creado con el comando:
   ```bash
   conda activate llm_example_repo_env
   
5. **Cambiar al Directorio del Repositorio**: Navega al directorio donde está clonado el repositorio utilizando el comando cd. Por ejemplo:    
    ```bash
    cd C:\Users\TuUsuario\Documents\llm_example_repo
    
6. **Instalar PDM**: Dentro del environment activado, instala PDM utilizando pip con el siguiente comando:
    ```bash
    pip install pdm

6. **Inicializar estructura con pdm**: Dentro del environment activado, pon el siguiente código:
    ```bash
    pdm init

7. **Instalar Dependencias con PDM**: Ejecuta pdm install para instalar todas las dependencias del proyecto definidas en el archivo pyproject.toml. Usa el siguiente comando:
    ```bash
    pdm install

8. **Abrir Anaconda Navigator**: Por ultimo, en anaconda navigator, nos dirigimos a la barra de navegacion superior, seleccionamos el
segundo dropdown, seleccionamos el ambiente, buscamos spyder, lo instalamos y lo abrimos.