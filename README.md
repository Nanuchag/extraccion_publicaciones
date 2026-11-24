# Pre-entrega 4: Extracción y almacenamiento seguro de datos vía API

## Descripción

Este proyecto realiza una petición HTTP `GET` a [JSONPlaceholder](https://jsonplaceholder.typicode.com/), una API pública de prueba. Recupera publicaciones, conserva los campos relevantes (`userId`, `id`, `title` y `body`) y almacena el resultado en `data_extracted.json`.

La configuración se obtiene desde variables de entorno mediante `python-dotenv`. El archivo `.env` se encuentra excluido del control de versiones por medio de `.gitignore`; se incluye `.env.example` como plantilla para reproducir la configuración.

## Tecnologías y dependencias

- Python 3.10 o superior.
- `requests`: realiza las peticiones HTTP.
- `python-dotenv`: carga la configuración desde `.env`.
- JSON: formato de almacenamiento de los datos.

## Estructura del repositorio

```text
pre-entrega-4-api/
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Excluye .env y archivos locales
├── README.md             # Instrucciones y documentación
├── data_extracted.json   # Resultado de una extracción
├── extract_data.py       # Script principal
└── requirements.txt      # Dependencias del proyecto
```

## Instalación y configuración

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/USUARIO/pre-entrega-4-api.git
   cd pre-entrega-4-api
   ```

2. Crear y activar un entorno virtual (recomendado):

   **Windows PowerShell**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux / macOS**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crear el archivo local `.env` a partir de la plantilla:

   **Windows PowerShell**

   ```powershell
   Copy-Item .env.example .env
   ```

   **Linux / macOS**

   ```bash
   cp .env.example .env
   ```

5. Revisar los valores de `.env`:

   ```env
   API_URL=https://jsonplaceholder.typicode.com/posts
   API_LIMIT=10
   REQUEST_TIMEOUT=10
   OUTPUT_FILE=data_extracted.json
   ```

   Esta API no requiere una clave de autenticación. De todas formas, la configuración se mantiene fuera del código para facilitar cambios y permitir incorporar credenciales en futuras integraciones sin hardcodearlas.

## Ejecución

Con el entorno virtual activo, ejecutar:

```bash
python extract_data.py
```

El script consulta la API y genera o actualiza `data_extracted.json` en la carpeta del proyecto. Para obtener más o menos publicaciones, modificar `API_LIMIT` en `.env`.

## Formato de salida

El archivo JSON contiene metadatos de la extracción y una lista con los registros obtenidos:

```json
{
    "source": "https://jsonplaceholder.typicode.com/posts",
    "extracted_at_utc": "fecha y hora de la extracción en UTC",
    "total_records": 10,
    "data": [
        {
            "userId": 1,
            "id": 1,
            "title": "Título de la publicación",
            "body": "Contenido de la publicación"
        }
    ]
}
```

## Manejo de errores

El programa contempla:

- Códigos HTTP fallidos mediante `raise_for_status()` y `HTTPError` (por ejemplo, 404 o 500).
- Tiempo de espera agotado (`Timeout`).
- Problemas de conexión (`ConnectionError`).
- Otros errores de petición (`RequestException`).
- Respuestas JSON con estructura inesperada o configuración inválida (`ValueError`).
- Errores de escritura del archivo (`OSError`).

En caso de error, informa el problema y finaliza con un código de salida distinto de cero.

## Seguridad

- No subir el archivo `.env` a GitHub.
- No escribir claves, tokens ni contraseñas directamente en el código.
- Mantener `.env.example` sin credenciales reales.
- No publicar información sensible dentro del archivo de salida.

## API utilizada

JSONPlaceholder: <https://jsonplaceholder.typicode.com/>

Endpoint: `GET https://jsonplaceholder.typicode.com/posts?_limit=10`


