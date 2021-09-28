<h1 align="center">ksp.py</h1>

<p align="center">
  <a href="https://www.codefactor.io/repository/github/adam757521/ksp.py"><img src="https://img.shields.io/codefactor/grade/github/adam757521/ksp.py?style=flat-square" /></a>
  <a href="https://pepy.tech/project/ksp.py"><img src="https://img.shields.io/pypi/dm/ksp.py?color=green&style=flat-square" /></a>
  <a href="https://pypi.org/project/ksp.py/"><img src="https://img.shields.io/pypi/v/ksp.py?style=flat-square" /></a>
  <a href=""><img src="https://img.shields.io/pypi/l/ksp.py?style=flat-square" /></a>
    <br/>
  <a href="https://ksppy.readthedocs.io/en/stable/">Documentation</a>
</p>

<p align="center">
   An API wrapper for KSP.
</p>

Features
-------------

- Fetch full product data easily (includes stock, tags, price, etc)
- Look for queries easily.
(MORE COMING SOON)

Installation
--------------

Installing ksp.py is very easy.

```sh
python -m pip install ksp.py
```

Examples
--------------

### Simple product stock viewer. ###

```py
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
```

TODO
--------------

- Add async support.

Known Issues
--------------

- Currently, None!

**Incase you do find bugs, please create an issue or a PR.**

Support
--------------

- **[Documentation](https://ksppy.readthedocs.io/en/stable/)**
