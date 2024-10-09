import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import OuterRef, Subquery

from translate.core.utils.logger import log
from translate.service.models import Translation


class Command(BaseCommand):
    """
    Export translations in the format:

    key,views,context,translation_de,translation_en,translation_fr,translation_it,translation_plural_de,
    translation_plural_en,translation_plural_fr,translation_plural_it
    """

    help = "Export database translations to CSV file in the bulk import format"

    @staticmethod
    def get_translation_subquery(language_code, plural=False):
        """Helper function to create a subquery for fetching translations."""
        if plural:
            return Subquery(
                Translation.objects.filter(key=OuterRef("key"), language__lang_info=language_code).values(
                    "translation_plural"
                )[:1]
            )
        else:
            return Subquery(
                Translation.objects.filter(key=OuterRef("key"), language__lang_info=language_code).values(
                    "translation"
                )[:1]
            )

    def export_csv(self):
        _DB_READ_PAGE_SIZE = 500
        _CSV_HEADER = [
            "key",
            "views",
            "context",
            "translation_de",
            "translation_en",
            "translation_fr",
            "translation_it",
            "translation_plural_de",
            "translation_plural_en",
            "translation_plural_fr",
            "translation_plural_it",
        ]

        file_name = Path("translations.csv")
        log.info(f"Exporting translations to {file_name.absolute()}")

        qs = (
            Translation.objects.exclude(key__snake_name__startswith="snake_name_")
            .order_by("key__snake_name")
            .values("key__snake_name", "key__usage_context", "key__views")
            .annotate(
                translation_de=self.get_translation_subquery("de"),
                translation_en=self.get_translation_subquery("en"),
                translation_fr=self.get_translation_subquery("fr"),
                translation_it=self.get_translation_subquery("it"),
                translation_plural_de=self.get_translation_subquery("de", plural=True),
                translation_plural_en=self.get_translation_subquery("en", plural=True),
                translation_plural_fr=self.get_translation_subquery("fr", plural=True),
                translation_plural_it=self.get_translation_subquery("it", plural=True),
            )
            .distinct("key__snake_name")
        )

        with file_name.open(mode="w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=_CSV_HEADER)
            writer.writeheader()

            for record in qs:
                writer.writerow(
                    {
                        "key": record["key__snake_name"],
                        "views": ":".join(record["key__views"]),
                        "context": record["key__usage_context"],
                        "translation_de": record["translation_de"] or "",
                        "translation_en": record["translation_en"] or "",
                        "translation_fr": record["translation_fr"] or "",
                        "translation_it": record["translation_it"] or "",
                        "translation_plural_de": record["translation_plural_de"] or "",
                        "translation_plural_en": record["translation_plural_en"] or "",
                        "translation_plural_fr": record["translation_plural_fr"] or "",
                        "translation_plural_it": record["translation_plural_it"] or "",
                    }
                )

        log.info("Export completed successfully!")

    def handle(self, *args, **options):
        """Handle command."""
        try:
            self.export_csv()
        except Exception as ex:
            log.error("An error occurred while exporting translations: %s", ex)

        log.info("Done!")
