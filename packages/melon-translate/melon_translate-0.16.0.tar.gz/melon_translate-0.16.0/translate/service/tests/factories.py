import random

import factory
from django.conf.locale import LANG_INFO

from translate.service import models


class TranslationFactory(factory.django.DjangoModelFactory):
    """Testing factory for ``Translation`` model."""

    class Meta:
        model = models.Translation

    translation = factory.Faker("bs")


class LanguageFactory(factory.django.DjangoModelFactory):
    """Testing factory for ``Language`` model."""

    class Meta:
        model = models.Language

    @factory.lazy_attribute
    def lang_info(self):
        """
        Generate random language info, but different
        from the one already available in the database.
        """
        all_lang_keys = set(LANG_INFO.keys())
        existing_lang_keys = set(models.Language.objects.values_list("lang_info", flat=True))
        available_lang_keys = list(all_lang_keys - existing_lang_keys)

        if not available_lang_keys:
            raise ValueError("No available language keys")

        return random.choice(available_lang_keys)


class TranslationKeyFactory(factory.django.DjangoModelFactory):
    """Testing factory for ``TranslationKey`` model."""

    class Meta:
        model = models.TranslationKey


class FakeLanguageFactory(factory.django.DjangoModelFactory):
    """
    Testing factory for ``Language`` model, but a fake one
    because we don't want to deal with the real languages
    that could already be present in the database.
    """

    class Meta:
        model = models.Language

    @factory.lazy_attribute
    def lang_info(self):
        """
        Generate random language info, but different
        from the one already available in the database.
        """
        import string

        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(4))
