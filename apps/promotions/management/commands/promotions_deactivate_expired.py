from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.promotions.models import Promotion


class Command(BaseCommand):
    help = "Deactivate promotions where active_before is in the past (active_before < today)."

    def handle(self, *args, **options):
        today = timezone.now().date()

        qs = Promotion.objects.filter(active=True, active_before__isnull=False, active_before__lt=today)
        count = qs.count()

        updated = qs.update(active=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Today={today}. Found={count}. Deactivated={updated}."
            )
        )
