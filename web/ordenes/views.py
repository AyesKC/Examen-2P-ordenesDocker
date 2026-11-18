from django.shortcuts import render
import requests
from .forms import OrdenForm
from django.shortcuts import redirect
from .forms_detalle import DetalleForm
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")


def lista_ordenes(request):

    try:

        respuesta = requests.get(
            f'{API_URL}/api/ordenes'
        )

        ordenes = respuesta.json()

    except Exception:
        ordenes = []

    return render(
        request,
        'ordenes/lista.html',
        {
            'ordenes': ordenes
        }
    )

def crear_orden(request):

    if request.method == 'POST':

        form = OrdenForm(request.POST)

        if form.is_valid():

            requests.post(
                f'{API_URL}/api/ordenes',
                json={
                    'cliente': form.cleaned_data['cliente'],
                    'estado': form.cleaned_data['estado']
                }
            )

            return redirect('/')

    else:

        form = OrdenForm()

    return render(
        request,
        'ordenes/crear.html',
        {
            'form': form
        }
    )

def editar_orden(request, id):

    respuesta = requests.get(
        f'{API_URL}/api/ordenes/{id}'
    )

    if respuesta.status_code != 200:

        return redirect('/')

    orden = respuesta.json()

    if request.method == 'POST':

        form = OrdenForm(request.POST)

        if form.is_valid():

            requests.put(
                f'{API_URL}/api/ordenes/{id}',
                json={
                    'cliente': form.cleaned_data['cliente'],
                    'estado': form.cleaned_data['estado']
                }
            )

            return redirect('/')

    else:

        form = OrdenForm(initial={
            'cliente': orden['cliente'],
            'estado': orden['estado']
        })

    return render(
        request,
        'ordenes/editar.html',
        {
            'form': form,
            'id': id
        }
    )

def eliminar_orden(request, id):

    requests.delete(
        f'{API_URL}/api/ordenes/{id}'
    )

    return redirect('/')

def detalles_orden(request, id):

    respuesta = requests.get(
        f'{API_URL}/api/ordenes/{id}/detalles'
    )

    detalles = respuesta.json()

    return render(
        request,
        'ordenes/detalles.html',
        {
            'detalles': detalles,
            'orden_id': id
        }
    )

def agregar_detalle(request, id):

    if request.method == 'POST':

        form = DetalleForm(request.POST)

        if form.is_valid():

            requests.post(
                f'{API_URL}/api/ordenes/{id}/detalles',
                json={
                    'producto': form.cleaned_data['producto'],
                    'cantidad': form.cleaned_data['cantidad'],
                    'precio_unitario': float(
                        form.cleaned_data['precio_unitario']
                    )
                }
            )

            return redirect(
                f'/detalles/{id}/'
            )

    else:

        form = DetalleForm()

    return render(
        request,
        'ordenes/agregar_detalle.html',
        {
            'form': form,
            'orden_id': id
        }
    )

def eliminar_detalle(request, detalle_id, orden_id):

    requests.delete(
        f'{API_URL}/api/detalles/{detalle_id}'
    )

    return redirect(
        f'/detalles/{orden_id}/'
    )

def editar_detalle(request, detalle_id, orden_id):

    respuesta = requests.get(
        f'{API_URL}/api/ordenes/{orden_id}/detalles'
    )

    detalles = respuesta.json()

    detalle_actual = None

    for detalle in detalles:

        if detalle['id'] == detalle_id:
            detalle_actual = detalle
            break

    if detalle_actual is None:
        return redirect(
            f'/detalles/{orden_id}/'
        )

    if request.method == 'POST':

        form = DetalleForm(request.POST)

        if form.is_valid():

            requests.put(
                f'{API_URL}/api/detalles/{detalle_id}',
                json={
                    'producto': form.cleaned_data['producto'],
                    'cantidad': form.cleaned_data['cantidad'],
                    'precio_unitario': float(
                        form.cleaned_data['precio_unitario']
                    )
                }
            )

            return redirect(
                f'/detalles/{orden_id}/'
            )

    else:

        form = DetalleForm(
            initial={
                'producto': detalle_actual['producto'],
                'cantidad': detalle_actual['cantidad'],
                'precio_unitario': detalle_actual['precio_unitario']
            }
        )

    return render(
        request,
        'ordenes/editar_detalle.html',
        {
            'form': form,
            'orden_id': orden_id
        }
    )
