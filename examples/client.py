import time

import ksp

client = ksp.Client(ksp.Languages.ENGLISH)
cache = []

while True:
    product = client.get_product(...)

    if product and product.stock:
        available_branches = [
            branch for branch, status in product.stock.items() if status
        ]

        for branch in available_branches:
            if branch not in cache:
                print(f"Branch '{branch}' has been resupplied!")

        for branch in cache:
            if branch not in available_branches:
                print(f"Branch '{branch}' ran out of stock!")

        cache = available_branches

    time.sleep(2)
