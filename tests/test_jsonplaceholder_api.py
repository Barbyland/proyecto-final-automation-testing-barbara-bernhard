import pytest
from pytest_check import check

from utils.logger import get_logger


logger = get_logger("api")


@pytest.mark.api
@pytest.mark.smoke
def test_get_post_existente_devuelve_json_valido(posts_api):
    logger.info("Ejecutando GET /posts/1")
    response = posts_api.get_post(1)
    body = response.json()

    check.equal(response.status_code, 200)
    check.equal(body["id"], 1)
    check.equal(body["userId"], 1)
    check.is_true(isinstance(body["title"], str))
    check.is_true(isinstance(body["body"], str))


@pytest.mark.api
@pytest.mark.regression
def test_post_crea_recurso_con_payload_externo(posts_api, post_data):
    logger.info("Ejecutando POST /posts")
    response = posts_api.create_post(
        post_data["title"],
        post_data["body"],
        post_data["userId"],
    )
    body = response.json()

    check.equal(response.status_code, 201)
    check.equal(body["title"], post_data["title"])
    check.equal(body["body"], post_data["body"])
    check.equal(body["userId"], post_data["userId"])
    check.is_in("id", body)


@pytest.mark.api
@pytest.mark.regression
def test_delete_post_devuelve_respuesta_exitosa(posts_api):
    logger.info("Ejecutando DELETE /posts/1")
    response = posts_api.delete_post(1)

    assert response.status_code == 200
    assert response.text == "{}"


@pytest.mark.api
@pytest.mark.regression
def test_get_post_inexistente_maneja_error_404(posts_api):
    logger.info("Ejecutando GET /posts/999999 para validar manejo de error")
    response = posts_api.get_post(999999)

    assert response.status_code == 404
    assert response.json() == {}
