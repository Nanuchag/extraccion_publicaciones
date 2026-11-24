"""Extrae publicaciones de JSONPlaceholder y las guarda en formato JSON."""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts").strip()
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "data_extracted.json").strip()
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
API_LIMIT = int(os.getenv("API_LIMIT", "10"))


def validate_configuration() -> None:
    """Valida la configuración antes de realizar la petición."""
    if not API_URL.startswith(("https://", "http://")):
        raise ValueError("API_URL debe comenzar con http:// o https://")
    if API_LIMIT < 1:
        raise ValueError("API_LIMIT debe ser un número entero mayor que cero")
    if REQUEST_TIMEOUT < 1:
        raise ValueError("REQUEST_TIMEOUT debe ser un número entero mayor que cero")
    if not OUTPUT_FILE:
        raise ValueError("OUTPUT_FILE no puede estar vacío")


def extract_posts() -> list[dict]:
    """Realiza una petición GET y devuelve publicaciones depuradas."""
    response = requests.get(
        API_URL,
        params={"_limit": API_LIMIT},
        timeout=REQUEST_TIMEOUT,
        headers={"Accept": "application/json"},
    )
    response.raise_for_status()

    payload = response.json()
    if not isinstance(payload, list):
        raise ValueError("La respuesta de la API no tiene el formato esperado (lista JSON).")

    cleaned_posts = []
    for item in payload:
        if not isinstance(item, dict):
            continue

        # Conservamos únicamente los campos relevantes para este ejercicio.
        cleaned_post = {
            "userId": item.get("userId"),
            "id": item.get("id"),
            "title": item.get("title"),
            "body": item.get("body"),
        }

        # Evitamos guardar registros incompletos.
        if all(value is not None for value in cleaned_post.values()):
            cleaned_posts.append(cleaned_post)

    return cleaned_posts


def save_json(posts: list[dict]) -> Path:
    """Guarda los registros y metadatos en un archivo JSON."""
    output_path = Path(OUTPUT_FILE)
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    export = {
        "source": API_URL,
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_records": len(posts),
        "data": posts,
    }

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(export, json_file, ensure_ascii=False, indent=4)

    return output_path


def main() -> int:
    try:
        validate_configuration()
        print(f"Consultando API: {API_URL}")
        posts = extract_posts()
        output_path = save_json(posts)
        print(f"Extracción finalizada: {len(posts)} registros guardados en {output_path}")
        return 0

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code if error.response is not None else "desconocido"
        print(f"Error HTTP ({status}): la API rechazó la solicitud. Detalle: {error}", file=sys.stderr)
    except requests.exceptions.Timeout:
        print("Error: se agotó el tiempo de espera al consultar la API.", file=sys.stderr)
    except requests.exceptions.ConnectionError:
        print("Error: no se pudo establecer conexión con la API. Verificá tu conexión.", file=sys.stderr)
    except requests.exceptions.RequestException as error:
        print(f"Error durante la petición a la API: {error}", file=sys.stderr)
    except (ValueError, json.JSONDecodeError) as error:
        print(f"Error de configuración o de formato de respuesta: {error}", file=sys.stderr)
    except OSError as error:
        print(f"Error al guardar el archivo: {error}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())


