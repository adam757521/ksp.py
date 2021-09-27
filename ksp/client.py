from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .http import HTTPClient
from .utils import get

if TYPE_CHECKING:
    from .enums import Languages
    from .product import Product

__all__ = ("Client",)


class Client:
    """
    Represents a KSP client.
    """

    __slots__ = ("http", "product_cache")

    def __init__(self, language: Languages):
        """
        :param Languages language: The language.
        """

        self.http = HTTPClient(language=language)
        self.product_cache = []

    def _add_products_to_cache(self, products: List[Product]) -> None:
        for product in products:
            if product not in self.product_cache:
                self.product_cache.append(product)

    def fetch_full_product(self, uin: int) -> Product:
        """
        Converts the partial product to a product.

        :param int uin: The partial uin.
        :return: The product.
        :rtype: Product
        """

        return self.http.get_product(uin)

    def get_product(self, uin: int) -> Optional[Product]:
        """
        Fetches the product.
        Returns the one in the cache if applicable.

        :param int uin: The product UIN.
        :return: The product if applicable.
        :rtype: Optional[Product]
        """

        cached_product = get(self.product_cache, uin=uin)

        if cached_product:
            return cached_product

        product = self.fetch_full_product(uin)

        if product:
            self._add_products_to_cache([product])

        return product

    def search(self, query: str) -> List[Product]:
        """
        Searches and finds products that match with the query.
        Returns products from the cache if applicable.

        :param str query: The query.
        :return: The products.
        :rtype: List[Product]
        """

        partial_products = self.http.search(query)

        products = [
            get(self.product_cache, uin=partial.uin)
            or self.fetch_full_product(partial.uin)
            for partial in partial_products
        ]
        self._add_products_to_cache(products)

        return products
