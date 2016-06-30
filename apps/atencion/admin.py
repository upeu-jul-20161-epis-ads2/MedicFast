from django.contrib import admin

from apps.atencion.models import AntecedenteMedico
from .models import Distrito, Provincia, Departamento, FuncionesVitales, Diagnostico, Producto, UnidadMedida, ReporteAtencion
from .models import DetalleReceta, Tratamiento, Consulta, Laboratorio, Historia, ConsultaEmergencia, Persona, Periodo,DiagnosticoConsulta
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
admin.site.register(Persona)
admin.site.register(Periodo)
admin.site.register(DiagnosticoConsulta)
admin.site.register(AntecedenteMedico)
admin.site.register(ReporteAtencion)