# Proyecto Final Automation Testing - Barbara Bernhard

Framework de automatizacion de pruebas desarrollado como entrega final del curso. El proyecto combina pruebas de interfaz web con Selenium WebDriver, pruebas de API con Requests, ejecucion con Pytest, datos externos, logging, screenshots automaticos y reportes HTML.

El objetivo es demostrar un framework mantenible, escalable e independiente, aplicando Page Object Model para UI y buenas practicas de organizacion de pruebas.

## Sitios y servicios utilizados

- UI: https://www.saucedemo.com/
- API: https://jsonplaceholder.typicode.com/

## Tecnologias

- Python 3.10+
- Pytest
- Selenium WebDriver
- Webdriver Manager
- Requests
- Pytest HTML
- Git y GitHub
- GitHub Actions

## Estructura del proyecto

```text
proyecto-final-automation-testing-barbara-bernhard/
  data/
    api_payloads.json
    ui_users.json
  pages/
    base_page.py
    cart_page.py
    checkout_page.py
    inventory_page.py
    login_page.py
  reports/
    automation.log
    reporte.html
    resultado_ejecucion.txt
  screenshots/
  tests/
    conftest.py
    test_jsonplaceholder_api.py
    test_saucedemo_ui.py
  utils/
    data_loader.py
    logger.py
  .github/workflows/tests.yml
  .gitignore
  pytest.ini
  requirements.txt
  README.md
```

## Casos automatizados de UI

- Login exitoso con usuario valido.
- Login negativo parametrizado con datos externos desde JSON.
- Validacion del catalogo, productos visibles, menu y filtro.
- Agregado del primer producto al carrito.
- Remocion de producto y validacion del contador.
- Checkout completo hasta finalizar la compra.

## Casos automatizados de API

- GET `/posts/1`: valida codigo 200, estructura y contenido JSON.
- POST `/posts`: crea un recurso usando payload externo desde JSON.
- DELETE `/posts/1`: valida respuesta exitosa del borrado.
- GET `/posts/999999`: valida manejo de error 404 para recurso inexistente.

## Instalacion

Desde la carpeta del proyecto:

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

Si ya tenes un entorno virtual activo:

```bash
python -m pip install -r requirements.txt
```

Verificar instalacion:

```bash
python -m pytest --version
```

## Ejecucion de pruebas

Ejecutar toda la suite:

```bash
python -m pytest -v --headless --html=reports/reporte.html --self-contained-html
```

Ejecutar solo API:

```bash
python -m pytest tests/test_jsonplaceholder_api.py -v --html=reports/reporte_api.html --self-contained-html
```

Ejecutar solo UI:

```bash
python -m pytest tests/test_saucedemo_ui.py -v --html=reports/reporte_ui.html --self-contained-html
```

Ejecutar UI en modo headless:

```bash
python -m pytest tests/test_saucedemo_ui.py -v --headless --html=reports/reporte_ui.html --self-contained-html
```

Ejecutar por markers:

```bash
python -m pytest -m smoke -v
python -m pytest -m regression -v
python -m pytest -m login -v
python -m pytest -m cart -v
python -m pytest -m checkout -v
python -m pytest -m api -v
```

## Reportes y evidencias

- Los reportes HTML se generan en la carpeta `reports/`.
- El log de ejecucion se genera en `reports/automation.log`.
- Si una prueba UI falla, se guarda una captura automatica en `screenshots/`.
- El nombre de cada captura incluye fecha, hora y nombre del test.

## Interpretacion de reportes

En el reporte HTML se puede revisar:

- Nombre de cada test ejecutado.
- Estado del resultado: passed, failed o skipped.
- Duracion de cada prueba.
- Detalle del error si una prueba falla.
- Captura asociada a la falla, cuando corresponde.

## Resultado de ejecucion local

La ultima ejecucion completa fue realizada en Windows con Python 3.10.7:

```text
11 passed in 295.98s
```

Detalle:

- 4 pruebas API passed.
- 7 pruebas UI passed.
- Reporte principal: `reports/reporte.html`.
- Resumen textual: `reports/resultado_ejecucion.txt`.

## CI/CD

El workflow `.github/workflows/tests.yml` ejecuta las pruebas en GitHub Actions ante cada push o pull request a la rama `main`. Tambien publica `reports/` y `screenshots/` como artefactos para revisar evidencias.

## Repositorio

Nombre sugerido por la consigna:

```text
proyecto-final-automation-testing-barbara-bernhard
```
