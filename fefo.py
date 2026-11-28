from datetime import date

def fefo(lotes, cantidad, hoy):
    """Selección FEFO (First Expired, First Out).

    Entrada: lotes (codigo, vencimiento, disponible) con código único,
    cantidad pedida (entero >= 0) y fecha actual.
    Salida: {"completo", "plan", "pendiente"}.

    Elegibilidad: el lote vence hoy o después y tiene disponible > 0.
    Orden: vencimiento ascendente y, si empatan, código ascendente
    (desempate reproducible).
    Política ante stock insuficiente: la reserva se RECHAZA (completo=False);
    no se reserva parcialmente ni se modifica el inventario. El plan parcial
    y la cantidad pendiente se devuelven solo como información para decidir
    esperar la reposición.
    Terminación: recorre como máximo L lotes.
    Tiempo O(L log L) por el ordenamiento (O(L) si ya vienen ordenados);
    espacio O(L).
    """
    if type(cantidad) is not int or cantidad < 0:
        raise ValueError("Cantidad invalida")
    if not isinstance(hoy, date):
        raise ValueError("Fecha invalida")
    candidatos = []
    codigos = set()
    for codigo, vencimiento, disponible in lotes:
        if not isinstance(codigo, str) or not codigo or codigo in codigos:
            raise ValueError("Codigo invalido o duplicado")
        codigos.add(codigo)
        if not isinstance(vencimiento, date) or type(disponible) is not int or disponible < 0:
            raise ValueError("Lote invalido")
        if vencimiento >= hoy and disponible > 0:
            candidatos.append((vencimiento, codigo, disponible))
    candidatos.sort()  # tuplas: (vencimiento, codigo) define el orden FEFO
    plan = []
    pendiente = cantidad
    for vencimiento, codigo, disponible in candidatos:
        if pendiente == 0:
            break
        tomar = min(pendiente, disponible)
        plan.append((codigo, tomar))
        pendiente -= tomar
    # El plan parcial es informativo: no se modifica el inventario.
    return {"completo": pendiente == 0, "plan": plan, "pendiente": pendiente}
