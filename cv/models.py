from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Perfil (models.Model):
    nombre = models.CharField (max_length = 100)
    
    cedula = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    edad = models.IntegerField(
        null=True,
        blank=True
    )
    
    nacionalidad = models.CharField(max_length=60, null=True, blank=True)


    fecha_de_nacimiento = models.DateField(
        null=True,
        blank=True
    )

    sexo = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    estado_civil = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    discapacidad = models.BooleanField(
        default=False
    )

    porcentaje_de_discapacidad = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    profesion = models.CharField (max_length = 100)
    descripcion = models.TextField ()
    
    perfil_activo = models.IntegerField(
        default=1
    )
    
    lugar_de_nacimiento = models.CharField(
        max_length=60,
        null=True,
        blank=True
    )
    
    licencia_de_conducir = models.CharField(
        max_length=6,
        null=True,
        blank=True
    )
    
    
    email = models.EmailField ()
    telefono = models.CharField (max_length = 20)
    
    telefono_convencional = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

    ubicacion = models.CharField (max_length = 100)
    
    direccion_de_trabajo = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    direccion_domiciliaria = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    
    sitio_web = models.URLField (blank = True)
    linkedin = models.URLField (blank = True)
    github = models.URLField (blank = True)
    foto = models.ImageField (upload_to = 'perfil/', blank = True, null = True)

    def __str__(self):
        return self.nombre

class Educacion (models.Model):
    institucion = models.CharField (max_length = 150)
    titulo = models.CharField (max_length = 150)
    fecha_inicio = models.DateField ()
    fecha_fin = models.DateField (blank = True, null = True)
    descripcion = models.TextField (blank = True)

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"

class Experiencia (models.Model):
    empresa = models.CharField (max_length = 150)
    cargo = models.CharField (max_length = 150)
    nombre_de_la_empresa = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    lugar_de_la_empresa = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    email_de_la_empresa = models.EmailField(
        max_length=100,
        null=True,
        blank=True
    )

    sitio_web_de_la_empresa = models.URLField(
        max_length=100,
        null=True,
        blank=True
    )

    # 👤 CONTACTO EMPRESARIAL
    nombre_del_contacto_empresarial = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    telefono_del_contacto_empresarial = models.CharField(
        max_length=60,
        null=True,
        blank=True
    )
    
    fecha_inicio = models.DateField ()
    fecha_fin = models.DateField (blank = True, null = True)
    descripcion = models.TextField ()
    
    # ⚙️ VISIBILIDAD EN FRONT
    activar_para_que_se_vea_en_front = models.BooleanField(
        default=True
    )

    # 📎 CERTIFICADO
    ruta_del_certificado = models.FileField(
        upload_to='certificados/experiencia/',
        null=True,
        blank=True
    )

    # 📌 ORDEN CRONOLÓGICO
    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.cargo} - {self.empresa or 'Empresa no definida'}"

    def __str__(self):
        return f"{self.cargo} - {self.empresa}"

class Habilidad (models.Model):
    nombre = models.CharField (max_length = 100)
    nivel = models.IntegerField (help_text = "Nivel del 1 al 5")

    def __str__(self):
        return self.nombre

class Certificado(models.Model):
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="certificados"
    )
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    fecha = models.DateField()

    # 🖼️ Imagen de presentación (preview)
    imagen = models.ImageField(
        upload_to="certificados/previews/",
        null=True,
        blank=True
    )

    # 📄 Archivo PDF real
    archivo = models.FileField(
        upload_to="certificados/pdf/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo

class Proyecto(models.Model):
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="proyectos"
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tecnologias = models.CharField(max_length=300)
    github = models.URLField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class VentaGarage(models.Model):

    ESTADO_PRODUCTO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]

    id_venta_garage = models.AutoField(
        primary_key=True
    )

    nombre_del_producto = models.CharField(
        max_length=100
    )

    estado_del_producto = models.CharField(
        max_length=40,
        choices=ESTADO_PRODUCTO_CHOICES
    )

    valor_del_bien = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    imagen_del_producto = models.ImageField(
        upload_to='venta_garage/',
        blank=True,
        null=True
    )

    activar_para_que_se_vea_enfront = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'venta_garage'
        verbose_name = 'Venta Garage'
        verbose_name_plural = 'Ventas Garage'
        ordering = ['nombre_del_producto']

    def __str__(self):
        return f"{self.nombre_del_producto} - ${self.valor_del_bien}"    

class Referencia(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"