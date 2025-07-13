from rest_framework import serializers
from .models import Room, MessageMetaData, MessageTextContent, MessageMediaContent

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type']

class MessageMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageMetaData
        fields = ['id', 'room', 'sender', 'sent_at']

class MessageTextContentSerializer(serializers.ModelSerializer):
    metadata = MessageMetaSerializer()

    class Meta:
        model = MessageTextContent
        fields = ['id', 'metadata', 'text']

class MessageMediaContentSerializer(serializers.ModelSerializer):
    metadata = MessageMetaSerializer()

    class Meta:
        model = MessageMediaContent
        fields = ['id', 'metadata', 'url']
