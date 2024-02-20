# Django Imports
from django.db import transaction

# DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Model Imports
from .models import Perk, Experience
from categories.models import Category
from experiences.models import Perk

# Serializer Imports
from . import serializers


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_id = request.data.get("category")
            if not category_id:
                raise exceptions.ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_id)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise exceptions.ParseError(
                        "The category kind should be 'experiences'."
                    )
            except Category.DoesNotExist:
                raise exceptions.NotFound("Category not found.")

            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)
                    perks = request.data.get("perks")
                    for perk_id in perks:
                        perk = Perk.objects.get(pk=perk_id)
                        experience.perks.add(perk)
                    return Response(
                        serializers.ExperienceDetailSerializer(experience).data
                    )
            except:
                raise exceptions.ParseError("Perk not found.")

        else:
            return Response(serializer.errors)


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
