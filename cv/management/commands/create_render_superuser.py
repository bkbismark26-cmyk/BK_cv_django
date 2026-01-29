import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Ensure exactly one superuser exists (the env-defined one)."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.WARNING("Superuser env vars not set; skipping."))
            return

        # 1) Crear o obtener el usuario objetivo (admin único)
        target, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        # Actualizar email si aplica
        if email and getattr(target, "email", "") != email:
            target.email = email

        # Forzar que sea admin
        target.is_staff = True
        target.is_superuser = True

        # Forzar contraseña (se sincroniza con ENV en cada deploy)
        target.set_password(password)
        target.save()

        # 2) Bajar a cualquier otro superuser
        demoted = User.objects.filter(is_superuser=True).exclude(pk=target.pk)\
                              .update(is_superuser=False, is_staff=False)

        msg = f"Unique superuser '{username}' ensured. Demoted {demoted} other superuser(s)."
        self.stdout.write(self.style.SUCCESS(msg))
