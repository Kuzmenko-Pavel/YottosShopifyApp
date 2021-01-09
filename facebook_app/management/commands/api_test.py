from django.core.management.base import BaseCommand, CommandError
from facebook_app.tasks import fb_test_call_api


class Command(BaseCommand):
    help = 'Run api test'

    def handle(self, *args, **options):
        fb_test_call_api()
