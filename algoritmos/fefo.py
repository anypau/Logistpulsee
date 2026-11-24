from datetime import date

def fefo(lotes, cantidad, hoy):
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
    candidatos.sort()
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
