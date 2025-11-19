# This file is intended to create initial boards :)

from django.core.management.base import BaseCommand
from forum.models import Board

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        boards = [
            ("1", "Anime", "a", "Anime & manga board"),
            ("2", "Random", "b", "Anything goes"),
            ("3", "Gaming", "g", "Gaming board"),
            ("4", "Technology", "t", "Technology board"),
            ("5", "Music", "m", "Music discussions"),
        ]

        for id, name, short, desc in boards:
            Board.objects.get_or_create(
                id=id, name=name, short_name=short, description=desc
            )

        self.stdout.write("Boards successfully loaded")
