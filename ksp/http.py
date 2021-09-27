from __future__ import annotations

from typing import List, Optional
from urllib import parse

import requests

from .enums import Languages, Sorts
from .product import PartialProduct, Product

__all__ = ("HTTPClient",)


class HTTPClient:
    """
    Represents an http client that handles requests to the API.
    """

    __slots__ = ("session", "language")

    BASE_URL = "https://ksp.co.il/m_action/api/"
    BASE_KSP_URL = "https://ksp.co.il/web/"

    def __init__(
        self, session: requests.Session = None, language: Languages = Languages.ENGLISH
    ) -> None:
        """
        :param requests.Session session: The requests session, will create one if not passed.
        :param language: The language, defaults to Languages.ENGLISH.
        """

        self.session = session or requests.Session()
        self.language = language

    @property
    def base_headers(self) -> dict:
        """
        Returns the base headers.

        :return: The base headers.
        :rtype: dict
        """

        return {
            "lang": self.language.value,
            "referer": self.BASE_KSP_URL + "web/",
        }

    def request(
        self, method: str, endpoint: str, headers: dict = None, query: dict = None
    ) -> Optional[dict]:
        """
        Sends a request to the endpoint and returns the response.
        Handles errors, etc.

        :param str method: The request method.
        :param str endpoint: The endpoint.
        :param dict headers: The headers.
        :param dict query: The query.
        :return: The response, if applicable.
        :rtype: Optional[dict]
        """

        query = query or {}
        headers = self.base_headers.update(headers) if headers else self.base_headers

        response = self.session.request(
            method=method,
            url=f"{self.BASE_URL}{endpoint}?{parse.urlencode(query)}",
            headers=headers,
        ).json()

        if "result" not in response or response["result"].get("status") == 404:
            return

        return response["result"]

    def get_product(self, uin: int) -> Optional[Product]:
        """
        Returns the product from the UID, if applicable.

        :param int uin: The UID.
        :return: The product, if applicable.
        :rtype: Optional[Product]
        """

        product_information = self.get_product_info(uin)

        if product_information:
            return Product.from_dict(product_information, self)

    def get_product_stock(self, sku: str) -> dict:
        """
        Returns the stock status of the product.

        :param str sku: The product SKU.
        :return: The product stock status.
        :rtype: dict
        """

        return self.request("GET", f"mlay/{sku}")

    def get_product_info(self, uin: int) -> dict:
        """
        Returns the full product information.

        :param int uin: The product unique identification number.
        :return: The product info.
        :rtype: dict
        """

        return self.request("GET", f"item/{uin}")

    def search_category(
        self, query: str, sort: Sorts = Sorts.HIGH_TO_LOW
    ) -> List[PartialProduct]:
        """
        Searches the category with the query and sort method.

        :param str query: The query.
        :param Sorts sort: The sort method, defaults to HIGH_TO_LOW.
        :return: The partial products.
        :rtype: List[PartialProduct]
        """

        response_json = self.request(
            "GET", "category/undefined", query={"search": query, "sort": sort.value}
        )

        return (
            [
                PartialProduct.from_dict(product_dict, self)
                for product_dict in response_json["result"]["items"]
            ]
            if response_json
            else []
        )

    def search(self, query: str) -> List[PartialProduct]:
        """
        Returns a list of partial products.

        :param str query: The query.
        :return: A list of partial products.
        :rtype: List[PartialProduct]
        """

        response_json = self.request("GET", "search/", query={"q": query})

        return (
            [
                PartialProduct.from_dict(product_dict, self)
                for product_dict in response_json["items"]
            ]
            if response_json
            else []
        )
