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

    ################################
    ##### LOGIN-REqUIRED TESTS #####
    ################################

    # Test --> Registered user creating a thread
    def test_reg_crt_thrd(self):
        self.client.login(username="testuser", password="123456")

        response = self.client.post(
            reverse("create_thread", args=[self.board.short_name]),
            {"title": "Test Thread", "description": "Thread description"}
        )

        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertEqual(Thread.objects.count(), 1)

        thread = Thread.objects.first()
        self.assertEqual(thread.title, "Test Thread")
        self.assertEqual(thread.user, self.user)
        self.assertEqual(thread.board, self.board)

    # Test --> Unregistered user creating a thread
    def test_unr_crt_thrd(self):
        response = self.client.post(
            reverse("create_thread", args=[self.board.short_name]),
            {"title": "Anon Thread", "description": "Should not work"}
        )

        # Expect redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

        # Should NOT create anything
        self.assertEqual(Thread.objects.count(), 0)

    # Test --> Registered user adding a comment
    def test_reg_add_cmnt(self):
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

        thread.refresh_from_db()
        self.assertEqual(thread.activity, 1)

    # Test --> Unregistered user adding a comment
    def test_unr_add_cmnt(self):
        thread = Thread.objects.create(
            board=self.board,
            user=self.user,
            title="Thread",
            description="Desc"
        )

        response = self.client.post(
            reverse("create_comment", args=[thread.id]),
            {"description": "Should not work"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

        self.assertEqual(Comment.objects.count(), 0)

    ####################################
    ##### NON-LOGIN-REqUIRED TESTS #####
    ####################################

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



