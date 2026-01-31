# admin.py
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import (
    Perfil, Educacion, Experiencia, Habilidad, Certificado, Proyecto, Referencia, VentaGarage,
    Reconocimiento, CursoRealizado, ProductoAcademico, ProductoLaboral
)

class EducacionInline(admin.TabularInline):
    model = Educacion
    extra = 0
    fields = ("institucion", "titulo", "fecha_inicio", "fecha_fin", "descripcion", "activar_para_que_se_vea_en_front")

class HabilidadInline(admin.TabularInline):
    model = Habilidad
    extra = 0
    fields = ("nombre", "nivel", "activar_para_que_se_vea_en_front")

class ReferenciaInline(admin.TabularInline):
    model = Referencia
    extra = 0
    fields = ("nombre", "empresa", "cargo", "telefono", "email", "descripcion", "activar_para_que_se_vea_en_front")


class ExperienciaInline(admin.StackedInline):
    model = Experiencia
    extra = 0
    fields = (
        "cargo", "empresa", "lugar_de_la_empresa", "email_de_la_empresa", "sitio_web_de_la_empresa",
        "fecha_inicio", "fecha_fin",
        "descripcion",  # ✅ ESTA ES LA QUE TE FALTA VER/EDITAR
        "activar_para_que_se_vea_en_front",
        "ruta_del_certificado"
    )

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 40})},
    }


class CursoInline(admin.TabularInline):
    model = CursoRealizado
    extra = 0

class ReconocimientoInline(admin.TabularInline):
    model = Reconocimiento
    extra = 0

class ProductoAcademicoInline(admin.TabularInline):
    model = ProductoAcademico
    extra = 0

class ProductoLaboralInline(admin.TabularInline):
    model = ProductoLaboral
    extra = 0

class VentaGarageInline(admin.TabularInline):
    model = VentaGarage
    extra = 0
    
class CertificadoInline(admin.TabularInline):
    model = Certificado
    extra = 0


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_completo", "email", "telefono", "perfil_activo")
    search_fields = ("nnombres", "apellidos", "email", "cedula")

    inlines = [
        EducacionInline,     # ✅
        ExperienciaInline,   # ✅
        HabilidadInline,     # ✅
        ReferenciaInline,    # ✅
        CursoInline,
        ReconocimientoInline,
        ProductoAcademicoInline,
        ProductoLaboralInline,
        VentaGarageInline,
        CertificadoInline,
    ]

    def nombre_completo(self, obj):
        return f"{obj.nnombres} {obj.apellidos}".strip()

    nombre_completo.short_description = "Nombre"
