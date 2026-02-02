from django.db import models
from django.conf import settings
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import MinValueValidator

def validar_fecha_no_futura(value):
    if value and value.year > date.today().year:
        raise ValidationError(
            "No se permite ingresar una fecha mayor al año actual."
        )

class Perfil (models.Model):
    nnombres = models.CharField(max_length=60, null=True, blank=True)
    apellidos = models.CharField(max_length=60, null=True, blank=True)
    
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
        blank=True,
        validators=[validar_fecha_no_futura]
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
            return f"{self.nnombres} {self.apellidos}".strip()

class Educacion(models.Model):
    perfil = models.ForeignKey(
        "Perfil",
        on_delete=models.CASCADE,
        related_name="educaciones"
    )

    institucion = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    fecha_inicio = models.DateField(validators=[validar_fecha_no_futura])
    fecha_fin = models.DateField(blank=True, null=True, validators=[validar_fecha_no_futura])
    descripcion = models.TextField(blank=True)

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)
    
    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError({
                    "fecha_fin": "La fecha de finalización no puede ser menor que la fecha de inicio."
                })

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"

class Experiencia(models.Model):
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="experiencias"
    )

    cargo = models.CharField(max_length=150)                # Excel: cargodesempenado
    empresa = models.CharField(max_length=150)              # Excel: nombrempresa

    lugar_de_la_empresa = models.CharField(max_length=50, null=True, blank=True)
    email_de_la_empresa = models.EmailField(max_length=100, null=True, blank=True)
    sitio_web_de_la_empresa = models.URLField(max_length=100, null=True, blank=True)

    nombre_del_contacto_empresarial = models.CharField(max_length=100, null=True, blank=True)
    telefono_del_contacto_empresarial = models.CharField(max_length=60, null=True, blank=True)

    fecha_inicio = models.DateField(validators=[validar_fecha_no_futura])                       # Excel: fechainiciogestion
    fecha_fin = models.DateField(blank=True, null=True, validators=[validar_fecha_no_futura])     # Excel: fechafingestion
    descripcion = models.TextField()                        # Excel: descripcionfunciones

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    ruta_del_certificado = models.FileField(
        upload_to='certificados/experiencia/',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-fecha_inicio']
    
    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError({
                    "fecha_fin": "La fecha de fin no puede ser menor que la fecha de inicio."
                })

    def __str__(self):
        return f"{self.cargo} - {self.empresa}"
    
class Reconocimiento(models.Model):
    TIPO_CHOICES = [
        ("Académico", "Académico"),
        ("Público", "Público"),
        ("Privado", "Privado"),
    ]

    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="reconocimientos")

    tipo_reconocimiento = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_reconocimiento = models.DateField(null=True, blank=True, validators=[validar_fecha_no_futura])
    descripcion_reconocimiento = models.TextField(blank=True)

    entidad_patrocinadora = models.CharField(max_length=150, null=True, blank=True)
    nombre_contacto_auspicia = models.CharField(max_length=120, null=True, blank=True)
    telefono_contacto_auspicia = models.CharField(max_length=40, null=True, blank=True)

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    ruta_certificado = models.FileField(
        upload_to="certificados/reconocimientos/",
        null=True, blank=True
    )

    class Meta:
        ordering = ["-fecha_reconocimiento"]

    def __str__(self):
        return f"{self.tipo_reconocimiento} - {self.perfil}"

class Habilidad(models.Model):
    perfil = models.ForeignKey(
        "Perfil",
        on_delete=models.CASCADE,
        related_name="habilidades"
    )

    nombre = models.CharField(max_length=100)
    nivel = models.IntegerField(help_text="Nivel del 1 al 5")

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

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
    fecha = models.DateField(validators=[validar_fecha_no_futura])
    
    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    # 🖼️ Imagen de presentación (preview)
    imagen = models.ImageField(
        upload_to="certificados/previews/",
        null=True,
        blank=True
    )

    # 📄 Archivo PDF real
    archivo = models.FileField(
        upload_to="certificados/pdf/",
        storage=RawMediaCloudinaryStorage(),  # ✅ RAW para PDFs
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True
    )
# ✅ NUEVO: Google Drive
    drive_file_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="ID del archivo en Google Drive (lo que va entre /d/ y /view)"
    )

    drive_share_url = models.URLField(
        null=True,
        blank=True,
        help_text="Link compartido de Drive (opcional si usas drive_file_id)"
    )

    def pdf_view_url(self):
        """
        URL para VER en navegador (Drive viewer).
        """
        if self.drive_file_id:
            return f"https://drive.google.com/file/d/{self.drive_file_id}/view?usp=sharing"
        return self.drive_share_url

    def pdf_download_url(self):
        """
        URL para DESCARGAR directo.
        """
        if self.drive_file_id:
            return f"https://drive.google.com/uc?export=download&id={self.drive_file_id}"
        # Si solo tienes share_url, igual se puede abrir; descarga depende de Drive
        return self.drive_share_url

    def __str__(self):
        return self.titulo

class CursoRealizado(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="cursos_realizados")

    nombre_curso = models.CharField(max_length=200)
    fecha_inicio = models.DateField(null=True, blank=True, validators=[validar_fecha_no_futura])
    fecha_fin = models.DateField(null=True, blank=True, validators=[validar_fecha_no_futura])

    total_horas = models.IntegerField(null=True, blank=True)
    descripcion_curso = models.TextField(blank=True)

    entidad_patrocinadora = models.CharField(max_length=150, null=True, blank=True)
    nombre_contacto_auspicia = models.CharField(max_length=120, null=True, blank=True)
    telefono_contacto_auspicia = models.CharField(max_length=40, null=True, blank=True)
    email_empresa_patrocinadora = models.EmailField(null=True, blank=True)

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    ruta_certificado = models.FileField(
        upload_to="certificados/cursos/",
        null=True, blank=True
    )

    class Meta:
        ordering = ["-fecha_inicio"]
        
    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError({
                    "fecha_fin": "La fecha de fin no puede ser anterior a la fecha de inicio."
                })

    def __str__(self):
        return self.nombre_curso
    
class ProductoAcademico(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="productos_academicos")

    nombre_recurso = models.CharField(max_length=200)
    clasificador = models.CharField(max_length=120, null=True, blank=True)
    descripcion = models.TextField(blank=True)

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_recurso

class ProductoLaboral(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="productos_laborales")

    nombre_producto = models.CharField(max_length=200)
    fecha_producto = models.DateField(null=True, blank=True, validators=[validar_fecha_no_futura])
    descripcion = models.TextField(blank=True)

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    class Meta:
        ordering = ["-fecha_producto"]

    def __str__(self):
        return self.nombre_producto

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
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="ventas_garage",
        null=True, blank=True
    )

    ESTADO_PRODUCTO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]

    nombre_del_producto = models.CharField(max_length=100)
    estado_del_producto = models.CharField(max_length=40, choices=ESTADO_PRODUCTO_CHOICES)

    descripcion = models.TextField(blank=True)  # Excel lo tiene

    valor_del_bien = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    imagen_del_producto = models.ImageField(upload_to='venta_garage/', blank=True, null=True)

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    class Meta:
        db_table = 'venta_garage'
        ordering = ['nombre_del_producto']

    def __str__(self):
        return f"{self.nombre_del_producto} - ${self.valor_del_bien}"    

class Referencia(models.Model):
    perfil = models.ForeignKey(
        "Perfil",
        on_delete=models.CASCADE,
        related_name="referencias"
    )

    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    descripcion = models.TextField(blank=True)

    activar_para_que_se_vea_en_front = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"
