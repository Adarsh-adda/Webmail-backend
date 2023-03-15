from rest_framework import serializers
from .models import User,Mail
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
    
# mail serializer
class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = '__all__'

    # put method
    def update(self, instance, validated_data):
        instance.starred = validated_data.get('starred', instance.starred)
        instance.save()
        return instance

class MyCustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

    


