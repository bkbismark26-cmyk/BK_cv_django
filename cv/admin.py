from django.contrib import admin
from .models import Perfil, Educacion, Experiencia, Habilidad, Certificado, Proyecto, Referencia, VentaGarage

admin.site.register (Perfil)
admin.site.register (Educacion)
admin.site.register (Experiencia)
admin.site.register (Habilidad)

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "institucion", "fecha")
    list_filter = ("institucion", "fecha")
    search_fields = ("titulo", "institucion")

admin.site.register (Proyecto)
admin.site.register (Referencia)
admin.site.register(VentaGarage)
