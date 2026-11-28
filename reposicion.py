def reposicion(disponible, en_orden, reservado, minimo, objetivo):
    """Regla de punto de pedido para un SKU.

    posicion = disponible + en_orden - reservado.
    Si posicion <= minimo se sugiere max(0, objetivo - posicion); si no, 0.
    Las órdenes abiertas ya cuentan en en_orden, por eso no se duplican
    sugerencias: al emitir una orden debe actualizarse en_orden antes de
    recalcular. Tiempo y espacio O(1).
    """
    valores = (disponible, en_orden, reservado, minimo, objetivo)
    if any(type(v) is not int or v < 0 for v in valores) or objetivo < minimo:
        raise ValueError("Parametros invalidos")
    posicion = disponible + en_orden - reservado
    sugerencia = max(0, objetivo - posicion) if posicion <= minimo else 0
    return posicion, sugerencia

def sugerencias(productos):
    """Aplica la regla a P productos, uno por uno (generador).

    Rechaza SKU duplicados para no sugerir dos veces el mismo producto.
    Tiempo O(P) esperado; espacio O(1) por SKU y O(P) para detectar
    duplicados.
    """
    # Una fila por SKU; las ordenes abiertas ya forman parte de en_orden.
    vistos = set()
    for sku, disponible, en_orden, reservado, minimo, objetivo in productos:
        if not isinstance(sku, str) or not sku or sku in vistos:
            raise ValueError("SKU invalido o duplicado")
        vistos.add(sku)
        posicion, cantidad = reposicion(disponible, en_orden, reservado, minimo, objetivo)
        yield sku, posicion, cantidad
