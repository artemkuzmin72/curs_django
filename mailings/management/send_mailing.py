from django.core.management.base import BaseCommand, CommandError
from main.models import Mailing
from main.utils import send_mailing


class Command(BaseCommand):
    help = "Отправляет рассылку вручную по ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            raise CommandError(f"Рассылка с ID={mailing_id} не найдена.")

        result = send_mailing(mailing)
        self.stdout.write(self.style.SUCCESS(result))