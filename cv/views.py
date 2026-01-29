from django.shortcuts import render
from .models import Perfil, Educacion, Experiencia, Habilidad, Referencia, VentaGarage

def cv_view (request):
    perfil = Perfil.objects.first ()
    educaciones = Educacion.objects.all ()
    experiencias = Experiencia.objects.all ()
    habilidades = Habilidad.objects.all ()
    referencias = Referencia.objects.all()
    
    ventas_garage = VentaGarage.objects.filter(
        activar_para_que_se_vea_enfront=True
    )

    context = {
        'perfil': perfil,
        'educaciones': educaciones,
        'experiencias': experiencias,
        'habilidades': habilidades,
        'certificados': perfil.certificados.all() if perfil else [],
        'proyectos': perfil.proyectos.all() if perfil else [],
        'referencias': referencias,
        'ventas_garage': ventas_garage,
    }

    return render (request, 'cv/cv.html', context)

