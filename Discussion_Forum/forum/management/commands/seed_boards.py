# This file is intended to create initial boards :)

from django.core.management.base import BaseCommand
from forum.models import Board

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        boards = [
            ("Anime", "a", "Anime & manga board"),
            ("Random", "b", "Anything goes"),
            ("Gaming", "g", "Gaming board"),
            ("Technology", "t", "Technology board"),
            ("Music", "m", "Music discussions"),
        ]

        for name, short, desc in boards:
            Board.objects.get_or_create(
                name=name, short_name=short, description=desc
            )

        self.stdout.write("Boards successfully loaded")
