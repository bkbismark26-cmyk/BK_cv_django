from django.shortcuts import render
from .models import (
    Perfil, Educacion, Experiencia, Habilidad, Certificado, Referencia, VentaGarage,
    Reconocimiento, CursoRealizado, ProductoAcademico, ProductoLaboral, Proyecto
)

def cv_view(request):
    perfil = Perfil.objects.first()

    # Si no hay perfil, evita errores
    if not perfil:
        return render(request, "cv/cv.html", {
            "perfil": None,
            "educaciones": [],
            "experiencias": [],
            "habilidades": [],
            "certificados": [],
            "proyectos": [],
            "referencias": [],
            "ventas_garage": [],
            "reconocimientos": [],
            "cursos_realizados": [],
            "productos_academicos": [],
            "productos_laborales": [],
        })

    educaciones = Educacion.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )
    
    experiencias = Experiencia.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )
    
    habilidades = Habilidad.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )
    
    certificados = Certificado.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )
    
    referencias = Referencia.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )

    ventas_garage = VentaGarage.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )

    reconocimientos = Reconocimiento.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )

    cursos_realizados = CursoRealizado.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )

    productos_academicos = ProductoAcademico.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )

    productos_laborales = ProductoLaboral.objects.filter(
        perfil=perfil,
        activar_para_que_se_vea_en_front=True
    )
    
    proyectos = Proyecto.objects.filter(
        perfil=perfil
    )

    context = {
        "perfil": perfil,
        "educaciones": educaciones,
        "experiencias": experiencias,
        "habilidades": habilidades,
        "certificados": certificados,
        "proyectos": proyectos,
        "referencias": referencias,
        "ventas_garage": ventas_garage,
        "reconocimientos": reconocimientos,
        "cursos_realizados": cursos_realizados,
        "productos_academicos": productos_academicos,
        "productos_laborales": productos_laborales,
    }

    return render(request, "cv/cv.html", context)

