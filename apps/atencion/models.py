"""Models lslsl."""

from django.db import models


estado_civil = (
    ('soltero', 'S'),
    ('casado', 'C'),
    ('divorciado', 'D'),
    ('viudo', 'V'),
    ('conviviente', 'Cn'),
)

sexo = (
    ('Femenino', 'F'),
    ('Masculino', 'M'),
)

ocupacion = (
    ('EstudianteFIA', 'EF'),
    ('EstudianteFCE', 'ECE'),
    ('EstudianteSALUD', 'ES'),
    ('EstudianteFACIHED', 'EED'),
    ('DocenteFIA', 'DF'),
    ('DocenteFCE', 'DCE'),
    ('DocenteSALUD', 'DS'),
    ('DocenteFACIHED', 'DED'),
    ('PersonalAdministrativo', 'PAd'),
    ('EstudianteCAT', 'EC'),
    ('DocenteCAT', 'DC'),
    ('Visitas', 'V'),
)
IMC = (
    ('PesoBajo', 'B'),
    ('PesoNormal', 'N'),
    ('Sobrepeso', 'S'),
    ('Obesidad', 'O'),
    ('ObesidadSevera', 'OS')
)

class Usuario(models.Model):
    """Class Model Usuario. """
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    dni = models.CharField(max_length=10)
    #image=models.ImageField(upload_to="", blank=True, null=True)
    sexo = models.CharField(max_length=20, choices=sexo)
    ocupacion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    codigo = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamento"

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento)
    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincia"

    def __str__(self):
        return self.nombre

class Distrito(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia)
    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distrito"

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    nombres = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=40)
    apellido_materno = models.CharField(max_length=40)
    dni = models.IntegerField(unique=True)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    estado_civil = models.CharField(max_length=20, choices=estado_civil)
    sexo = models.CharField(max_length=20, choices=sexo)
    telefono = models.IntegerField()
    ocupacion = models.CharField(max_length=20, choices=ocupacion)
    direccion_actual = models.CharField(max_length=100)
    distrito = models.ForeignKey(Distrito)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
    def __str__(self):
        return "%s" %self.numero

class Historia(models.Model):
    persona = models.OneToOneField(Persona)
    numero = models.IntegerField(unique=True)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Historia"
        verbose_name_plural = "Historias"
    def __str__(self):
        return "%s" %self.numero

class Consulta(models.Model):
    #usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField(auto_now_add=True)
    antecedentes = models.TextField()
    enfermedad_actual = models.TextField()
    examen_fisico = models.TextField()
    historia = models.ForeignKey(Historia)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
    def __str__(self):
        return self.enfermedad_actual
        
class FuncionesVitales(models.Model):
    frecuencia_cardiaca = models.IntegerField()
    frecuencia_respiratoria = models.IntegerField()
    presion_arterial = models.IntegerField()
    temperatura = models.IntegerField()
    peso = models.IntegerField()
    talla = models.IntegerField()
    masa_corporal = models.IntegerField()
    diagnostico_mc = models.CharField(max_length=15, choices=IMC, default='N')
    consulta = models.ForeignKey(Consulta)
    class Meta:
        verbose_name = "Funciones Vitales"
        verbose_name_plural = "Funciones Vitales"
    def __str__(self):
        return self.diagnostico_mc




class Diagnostico(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    consulta =models.ForeignKey(Consulta)
    class Meta:
        verbose_name = "Diagnostico"
        verbose_name_plural = "Diagnosticos"
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=100)
    stock = models.IntegerField()
    precio_compra = models.FloatField()
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.descripcion

class UnidadMedida(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
    def __str__(self):
        return self.nombre


class Tratamiento(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    recomendacion = models.TextField()
    consulta = models.ForeignKey(Consulta)

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"
    def __str__(self):
        return "%s" % self.fecha

class DetalleReceta(models.Model):
    precio_venta = models.FloatField()
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField()
    presentacion = models.ForeignKey(UnidadMedida)
    importe = models.FloatField()
    dosis = models.IntegerField()
    periodo = models.IntegerField()
    tratamiento = models.ForeignKey(Tratamiento)
    class Meta:
        verbose_name = "Detalle de Receta"
        verbose_name_plural = "Detalles de Receta"
    def __str__(self):
        return self.producto.descripcion




class Periodo(models.Model):
    ciclo = models.CharField(unique=True, max_length=10)
    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"
    def __unicode__(self):
        return self.ciclo


class Laboratorio(models.Model):
    hemoglobina = models.IntegerField()
    endocritos = models.IntegerField()
    globulos_rojos = models.IntegerField()
    globulos_blancos = models.IntegerField()
    tipo_sangre = models.CharField(max_length=10)
    periodo = models.ForeignKey(Periodo)
    historia = models.ForeignKey(Historia)

    class Meta:
        verbose_name = "Prueba de Laboratorio"
        verbose_name_plural = "Pruebas de Laboratorio"
    def __unicode__(self):
        return self.hemoglobina


class ConsultaEmergencia(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    historia = models.ForeignKey(Historia)
    class Meta:
        verbose_name = "Consulta por Emergencia"
        verbose_name_plural = "Consultas por Emergencia"
    def __str__(self):
        return self.historia.nombres