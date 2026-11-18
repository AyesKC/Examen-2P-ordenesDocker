from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('crear/', views.crear_orden, name='crear_orden'),
    path('editar/<int:id>/', views.editar_orden, name='editar_orden'),
    path('eliminar/<int:id>/', views.eliminar_orden, name='eliminar_orden'),
    path('detalles/<int:id>/', views.detalles_orden, name='detalles_orden'),
    path('detalles/<int:id>/agregar/', views.agregar_detalle,name='agregar_detalle'),
    path('detalle/eliminar/<int:detalle_id>/<int:orden_id>/',views.eliminar_detalle,name='eliminar_detalle'),
    path('detalle/editar/<int:detalle_id>/<int:orden_id>/',views.editar_detalle,name='editar_detalle'),
]
