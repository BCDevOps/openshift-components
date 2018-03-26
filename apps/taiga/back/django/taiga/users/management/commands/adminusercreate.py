from django.core.management.base import BaseCommand, CommandError
from django.core.management import CommandError
from django.core.management import call_command
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crate a superuser, and allow password to be provided'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument(
            '--username', dest='username', default=None,
            help='Specifies the username for the superuser.',
        )

        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )
        parser.add_argument(
            '--preserve', dest='preserve', default=False, action='store_true',
            help='Exit normally if the user already exists.',
        )

    def handle(self, *args, **options):
        password = options.get('password')
        username = options.get('username')
        database = options.get('database')

        if password and not username:
            raise CommandError("--username is required if specifying --password")

        if username and options.get('preserve'):
            exists = get_user_model()._default_manager.db_manager(database).filter(username=username).exists()
            if exists:
                self.stdout.write("User exists, exiting normally due to --preserve")
                return
            else:
                call_command('loaddata', 'initial_user')

        if password:
            user = get_user_model()._default_manager.db_manager(database).get(username=username)
            user.set_password(password)
            user.save()
