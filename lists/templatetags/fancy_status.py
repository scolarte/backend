from django import template

register = template.Library()

@register.filter(name="fancy_status_list")
def fancy_status(value):
    if value == "recibida_no_pagada":
        status = "Creada"
    if value == "en_revision":
        status = "En Revision"
    if value == "recibida_pagada":
        status = "Confirmada"
    if value == "en_camino":
        status = "En Camino"
    if value == "entregada":
        status = "Entregada"
    if value == "cancelada":
        status = "Cancelada"
    return status

@register.filter(name="fancy_status_class")
def fancy_status_class(value):
    if value == "recibida_no_pagada":
        status = "info"
    if value == "en_revision":
        status = "warning"
    if value == "recibida_pagada":
        status = "primary"
    if value == "en_camino":
        status = "secondary"
    if value == "entregada":
        status = "success"
    if value == "cancelada":
        status = "danger"
    return status

@register.filter(name="fancy_status_message")
def fancy_status_message(value):
    if value == "recibida_no_pagada":
        status = "Cuando completes la lista, pulsa en el boton comprar para que un agente la revise"
    if value == "en_revision":
        status = "Un miembro de nuestro equipo esta revisando la lista"
    if value == "recibida_pagada":
        status = "Se ha confirmado el pago de la lista, se esta procesando la entrega"
    if value == "en_camino":
        status = "Tu pedido esta en camino!"
    if value == "entregada":
        status = "Tu lista fue entregada"
    if value == "cancelada":
        status = "Tu lista fue cancelada"
    return status