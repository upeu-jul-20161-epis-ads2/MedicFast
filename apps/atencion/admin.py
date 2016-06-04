from django.contrib import admin
from .models import Distrito, Provincia, Departamento,  FuncionesVitales, Diagnostico, Producto, UnidadMedida
from .models import DetalleReceta, Tratamiento, Consulta, Laboratorio, Historia, ConsultaEmergencia
# Register your models here.

admin.site.register(Distrito)
admin.site.register(Provincia)
admin.site.register(Departamento)
admin.site.register(FuncionesVitales)
admin.site.register(Diagnostico)
admin.site.register(Producto)
admin.site.register(UnidadMedida)
admin.site.register(DetalleReceta)
admin.site.register(Tratamiento)
admin.site.register(Consulta)
admin.site.register(Laboratorio)
admin.site.register(Historia)
admin.site.register(ConsultaEmergencia)
