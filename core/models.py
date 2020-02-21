from account.models import User
from django.db.models import (
    Model, TextField, DateTimeField, ForeignKey, CASCADE)
from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def deserialize_user(user):
    return {
        'id': user.id, 'email': user.email,
        'first_name': user.first_name, 'last_name': user.last_name
    }


class TrackableDate(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Message(TrackableDate):
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(User, on_delete=CASCADE,
                           verbose_name='recipient', related_name='to_user', db_index=True)
    body = TextField(max_length=2000, null=True)

    def __str__(self):
        return '{} {}'.format(self.id, self.body)

    def to_json(self):
        images = []
        msg = {'body': self.body, 'id': self.id, 'created_at': str(
            self.created_at), 'updated_at': str(self.updated_at)}
        for i in self.images.all():
            a = {}
            a['message'] = i.id
            a['image'] = i.image.url
            images.append(a)
        msg['images'] = images
        return msg

    def characters(self):
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {'type': 'recieve_group_message', 'user': deserialize_user(
            self.user), 'message': self.to_json()}
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)(
            "{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        if self.body:
            self.body = self.body.strip()  # Trimming whitespaces from the body
        super(Message, self).save(*args, **kwargs)

    class Meta:
        app_label = 'core'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-created_at',)


def nameFile(instance, filename):
    return '/'.join(['message_images', filename])


class Image(Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to=nameFile, max_length=254, blank=True, null=True)

    def __str__(self):
        return "{} | {}".format(self.message.body, self.image)
