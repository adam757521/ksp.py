from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .http import HTTPClient

__all__ = (
    "ProductFlag",
    "ProductDeliveryFlag",
    "ProductTag",
    "Product",
    "PartialProduct",
)


@dataclass
class ProductFlag:
    """
    Represents a product flag.

    :ivar str type: The flag type.
    :ivar str name: The flag name.
    """

    type: str
    name: str

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> ProductFlag:
        """
        Creates a dictionary to a product flag.

        :param Dict[str, str] dictionary: The dictionary
        :return: The product flag.
        :rtype: ProductFlag
        """

        return cls(dictionary["type"], dictionary["name"])


@dataclass
class ProductDeliveryFlag(ProductFlag):
    """
    Represents a product delivery flag.

    :ivar str type: The flag type.
    :ivar str name: The flag name.
    :ivar str place: The flag place.
    :ivar int price: The flag price
    :ivar Dict[str, int] time: The flag time.
    """

    place: str
    price: int
    time: ProductDeliveryTime

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> ProductDeliveryFlag:
        """
        Creates a dictionary to a product delivery flag.

        :param Dict[str, str] dictionary: The dictionary
        :return: The product delivery flag.
        :rtype: ProductDeliveryFlag
        """

        return cls(
            dictionary["type"],
            dictionary["title"],
            dictionary["place"],
            int(dictionary["price"] or 0),
            ProductDeliveryTime.from_dict(dictionary["time"]),
        )


@dataclass
class ProductDeliveryTime:
    """
    Represents a product delivery time.
    """

    min: Optional[int]
    max: Optional[int]

    @classmethod
    def from_dict(cls, dictionary: Dict[str, int]) -> ProductDeliveryTime:
        """
        Creates a ProductDeliveryTime object from the dict.

        :param Dict[str, Optional[int]] dictionary: The dictionary.
        :return: The product delivery time object.
        :rtype: ProductDeliveryTime
        """

        return cls(*[int(value) if value else None for value in dictionary.values()])


@dataclass
class ProductTag:
    """
    Represents a product tag.

    :ivar str name: The tag name.
    :ivar str description: The tag description.
    """

    name: str
    description: str

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> ProductTag:
        """
        Creates a dictionary to a product tag.

        :param Dict[str, str] dictionary: The dictionary
        :return: The product tag.
        :rtype: ProductTag
        """

        return cls(dictionary["up_name"], dictionary["tag_name"])


@dataclass
class PartialProduct:
    """
    Represents a partial KSP product.

    :ivar HTTPClient http: The HTTP client.
    :ivar str images: A list of product images.
    :ivar str name: The product name.
    :ivar int price: The product price in shekels.
    :ivar int uin: The unique id of the product.
    :ivar str sku: The SKU of the product.
    """

    http: HTTPClient
    images: List[str]
    name: str
    price: int
    uin: int
    sku: str

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str], http: HTTPClient) -> PartialProduct:
        """
        Creates a partial product from a dictionary.

        :param HTTPClient http: The HTTP client.
        :param Dict[str, str] dictionary: The dictionary.
        :return: The partial product.
        :rtype: PartialProduct
        """

        return cls(
            http,
            [dictionary["img"]],
            dictionary["name"],
            int(dictionary["price"]),
            int(dictionary["uin"]),
            dictionary["uinsql"],
        )


@dataclass
class Product(PartialProduct):
    """
    Represents a KSP product.

    :ivar HTTPClient http: The HTTP client.
    :ivar List[str] images: The images.
    :ivar str name: The product name.
    :ivar int price: The product price.
    :ivar int uin: The product unique identification number.
    :ivar str sku: The product SKU.
    :ivar int max_payments: The product max payments.
    :ivar str description: The product description.
    :ivar List[ProductFlag] benefits: The product benefits.
    :ivar List[ProductDeliveryFlag] delivery_flags: The product delivery flags.
    :ivar List[ProductFlag] flags: The product flags.
    :ivar List[ProductTag] tags: The product tags.
    :ivar List[int] variants: All variants of the product.
    :ivar ProductTag note: The note of the product.
    """

    max_payments: int
    description: str
    benefits: List[ProductFlag]
    delivery_flags: List[ProductDeliveryFlag]
    flags: List[ProductFlag]
    tags: List[ProductTag]
    variants: List[int]
    note: Optional[ProductTag] = None

    @property
    def stock(self) -> Dict[str, bool]:
        """
        Returns the stock of the product.

        :return: The stock.
        :rtype: Dict[str, bool]
        """

        return {
            branch["name"]: 0 < branch["qnt"]
            for branch in self.http.get_product_stock(self.sku).values()
        }

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any], http: HTTPClient) -> Product:
        """
        Creates a product from a dictionary.

        :param HTTPClient http: The HTTP client.
        :param Dict[str, Any] dictionary: The dictionary.
        :return: The product.
        :rtype: Product
        """

        note = dictionary["redMsg"]

        return cls(
            http,
            list(dictionary["images"].values()),
            dictionary["data"]["name"],
            dictionary["data"]["price"],
            dictionary["data"]["uin"],
            dictionary["data"]["uinsql"],
            dictionary["p"],
            dictionary["data"]["smalldesc"],
            [
                ProductFlag.from_dict(benefit)
                for benefit in dictionary["benefitBox"].values()
            ],
            [
                ProductDeliveryFlag.from_dict(delivery_flag)
                for delivery_flag in dictionary["delivery"]
            ],
            [ProductFlag.from_dict(flag) for flag in dictionary["flags"].values()],
            [ProductTag.from_dict(tag) for tag in dictionary["tags"]],
            [
                int(variation["uin_item"])
                for variation in dictionary["products_options"]["variations"]
            ]
            if "products_options" in dictionary
            else [],
            ProductTag(note["type"], note["msg"]) if note else None,
        )
