def reposicion(disponible, en_orden, reservado, minimo, objetivo):
    valores = (disponible, en_orden, reservado, minimo, objetivo)
    if any(type(v) is not int or v < 0 for v in valores) or objetivo < minimo:
        raise ValueError("Parametros invalidos")
    posicion = disponible + en_orden - reservado
    sugerencia = max(0, objetivo - posicion) if posicion <= minimo else 0
    return posicion, sugerencia

def sugerencias(productos):
    # Una fila por SKU; las ordenes abiertas ya forman parte de en_orden.
    vistos = set()
    for sku, disponible, en_orden, reservado, minimo, objetivo in productos:
        if not isinstance(sku, str) or not sku or sku in vistos:
            raise ValueError("SKU invalido o duplicado")
        vistos.add(sku)
        posicion, cantidad = reposicion(disponible, en_orden, reservado, minimo, objetivo)
        yield sku, posicion, cantidad
