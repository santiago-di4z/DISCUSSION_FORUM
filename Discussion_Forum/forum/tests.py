from django.test import TestCase, Client
from django.urls import reverse
from forum.models import Board, Thread, Comment
from django.contrib.auth import get_user_model
User = get_user_model()

class ForumTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.board = Board.objects.create(short_name="tst", name="Test Board")

    # Test --> Create a New Threat
    def test_crt_thrd(self):
        self.client.login(username="testuser", password="123456")

        response = self.client.post(
            reverse("create_thread", args=[self.board.short_name]),
            {"title": "Test Thread", "description": "Thread description"}
        )

        # Must redirect to the detail page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Thread.objects.count(), 1)

        thread = Thread.objects.first()
        self.assertEqual(thread.title, "Test Thread")
        self.assertEqual(thread.user, self.user)
        self.assertEqual(thread.board, self.board)

    # Test --> Add Comment
    def test_add_cmnt(self):
        self.client.login(username="testuser", password="123456")

        thread = Thread.objects.create(
            board=self.board,
            user=self.user,
            title="Thread",
            description="Desc"
        )

        response = self.client.post(
            reverse("create_comment", args=[thread.id]),
            {"description": "My comment"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        self.assertEqual(comment.thread, thread)
        self.assertEqual(comment.user, self.user)

        # Activity must increase
        thread.refresh_from_db()
        self.assertEqual(thread.activity, 1)

    # Test --> Show Boards
    def test_shw_brds(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.board.name)

    # Test --> Popular & New Threads
    def test_pplr_new(self):
        # Create 2 threads
        t1 = Thread.objects.create(board=self.board, user=self.user, title="T1", description="D1", activity=5)
        t2 = Thread.objects.create(board=self.board, user=self.user, title="T2", description="D2", activity=0)

        response = self.client.get(reverse("board_detail", args=[self.board.short_name]))

        self.assertEqual(response.status_code, 200)

        # Must be in the page
        self.assertContains(response, "T1") # T1 must be in popular
        self.assertContains(response, "T2") # T2 must be in new

    # Test --> OP tag in the comments
    def test_op_tag(self):
        self.client.login(username="testuser", password="123456")

        thread = Thread.objects.create(
            board=self.board,
            user=self.user,
            title="Thread",
            description="Desc"
        )

        # OP's comment
        Comment.objects.create(thread=thread, user=self.user, description="OP here!")

        response = self.client.get(reverse("thread_detail", args=[thread.id]))

        # OP must appear in the HTML
        self.assertContains(response, "OP")



