from rest_framework import serializers

from toyss.models import Toy


class ToySerializer(serializers.ModelSerializer):
  class Meta:
    model = Toy
    fields = ('id',
              'created',
              'name',
              'description',
              'toy_category',
              'release_date',
              'was_included_in_home')


def create(self, validated_data):
  """
  "Create a new Toy object, and return it."

  The **validated_data argument is a dictionary of all the validated data that we want to create a new Toy object with

  :param self:
  :param validated_data: The validated data from the serializer
  :return: The Toy object is being returned.
  """
  return Toy.objects.create(**validated_data)


def update(self, instance, validated_data):
  """
  It updates the instance with the validated data

  :param self:
  :param instance: The current instance of the object that the serializer is bound to
  :param validated_data: The data that was validated by the serializer
  :return: The instance is being returned.
  """
  instance.name = validated_data.get('name', instance.name)
  instance.description = validated_data.get('description', instance.description)
  instance.toy_category = validated_data.get('toy_category', instance.toy_category)
  instance.release_date = validated_data.get('release_date', instance.release_date)
  instance.was_included_in_home = validated_data.get('was_included_in_home', instance.was_included_in_home)
  instance.save()
  return instance
