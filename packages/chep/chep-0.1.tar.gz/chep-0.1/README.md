
# chep

Este paquete permite extraer el puerto SSH desde el estado del servicio `chep` ejecutado con `systemctl`.

## Instalación

Instálalo directamente desde PyPI con:

```bash
pip install chep
```

## Uso

```python
from chep import chep

puerto = chep()
print(puerto)
```
