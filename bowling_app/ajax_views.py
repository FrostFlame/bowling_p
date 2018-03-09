from dal import autocomplete

from accounts.models import City


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.name

    def get_queryset(self):
        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
