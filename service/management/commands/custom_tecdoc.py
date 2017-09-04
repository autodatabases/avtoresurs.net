from django.core.management import BaseCommand





class Command(BaseCommand):
    help = 'Adding custom crosses 2 TECDOC'

    def handle(self, *args, **options):
        self.pro_exhaust()

    def pro_exhaust(self):
        pass