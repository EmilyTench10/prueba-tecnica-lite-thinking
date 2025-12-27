from django.core.management.base import BaseCommand
from apps.blockchain.models import RegistroBlockchain


class Command(BaseCommand):
    help = 'Elimina todos los registros de la blockchain para reiniciar la cadena'

    def handle(self, *args, **options):
        count = RegistroBlockchain.objects.count()
        RegistroBlockchain.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Se eliminaron {count} registros de la blockchain')
        )
        self.stdout.write(
            self.style.SUCCESS('La blockchain ha sido reiniciada. Los nuevos registros tendrán hashes válidos.')
        )
