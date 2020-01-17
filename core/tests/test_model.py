from django.db import IntegrityError
from django.test import TestCase
from core.models import Message
from account.models import User


class MessageTestCase(TestCase):
    """
    Toy model test cases (there isn't much bussine logic).
    """

    def setUp(self):
        self.test_user1 = User.objects.create(email='bart')
        self.test_user2 = User.objects.create(email='milhouse')

    def test_message_user(self):
        msg = Message.objects.create(user=self.test_user2,
                                     recipient=self.test_user1,
                                     body='test')
        self.assertEqual(msg.user.email, 'milhouse')

    def test_message_body(self):
        msg = Message.objects.create(user=self.test_user1,
                                     recipient=self.test_user2,
                                     body='123')
        self.assertEqual(msg.body, '123')

    def test_message_characters(self):
        msg = Message.objects.create(user=self.test_user1,
                                     recipient=self.test_user2,
                                     body='a')
        self.assertEqual(msg.characters(), 1)

    def test_message_body_strip(self):
        msg = Message.objects.create(user=self.test_user1,
                                     recipient=self.test_user2,
                                     body=' aaa ')
        self.assertEqual(msg.body, 'aaa')

    def test_message_no_user(self):
        with self.assertRaises(IntegrityError):
            Message.objects.create(user=None, body='test')

    def test_message_create_retrieve(self):
        mid = Message.objects.create(user=self.test_user1,
                                     recipient=self.test_user2,
                                     body='tbody').id
        msg = Message.objects.get(id=mid)
        # Asserts
        self.assertEqual(msg.characters(), 5)
        self.assertEqual(msg.body, 'tbody')
        self.assertEqual(msg.user, self.test_user1)
        self.assertEqual(msg.recipient, self.test_user2)
