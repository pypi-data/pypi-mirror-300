from django.test import TestCase
from eveuniverse.models import EveType

from metenox.api.fuzzwork import get_type_ids_prices
from metenox.models import EveTypePrice
from metenox.tests.testdata.load_eveuniverse import load_eveuniverse


class TestFuzzWork(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_eveuniverse()

    def test_crash_empty_search_query(self):
        """
        With an empty search query the API returns [] instead of a dict.
        This makes the code crash whe calling .items() on the result
        """

        get_type_ids_prices([])

    def test_no_price_update_on_zero(self):
        """
        If the new price of an eve type is zero it is refused
        """

        eve_type = EveType.objects.get(id=16634)
        type_price = EveTypePrice.objects.create(eve_type=eve_type, price=10_000)

        type_price.update_price(0)

        self.assertEqual(type_price.price, 10_000)
