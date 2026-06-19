import requests
import pytest

from utils.data_loader import load_json
from utils.logger import get_logger


BASE_URL = "https://jsonplaceholder.typicode.com"
payloads = load_json("api_payloads.json")
logger = get_logger("api")


@pytest.mark.api
@pytest.mark.smoke
def test_get_post_existente_devuelve_json_valido():
    logger.info("Ejecutando GET /posts/1")
    response = requests.get(f"{BASE_URL}/posts/1", timeout=10)
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == 1
    assert body["userId"] == 1
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)


@pytest.mark.api
@pytest.mark.regression
def test_post_crea_recurso_con_payload_externo():
    logger.info("Ejecutando POST /posts")
    payload = payloads["new_post"]
    response = requests.post(f"{BASE_URL}/posts", json=payload, timeout=10)
    body = response.json()

    assert response.status_code == 201
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


@pytest.mark.api
@pytest.mark.regression
def test_delete_post_devuelve_respuesta_exitosa():
    logger.info("Ejecutando DELETE /posts/1")
    response = requests.delete(f"{BASE_URL}/posts/1", timeout=10)

    assert response.status_code == 200
    assert response.text == "{}"


@pytest.mark.api
@pytest.mark.regression
def test_get_post_inexistente_maneja_error_404():
    logger.info("Ejecutando GET /posts/999999 para validar manejo de error")
    response = requests.get(f"{BASE_URL}/posts/999999", timeout=10)

    assert response.status_code == 404
    assert response.json() == {}
