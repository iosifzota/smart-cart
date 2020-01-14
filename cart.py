#!/usr/bin/env python

import time


class Product:
    def __init__(self, name, code, price):
        self._name = name
        self._code = code
        self._price = price

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, productPrice):
        self._price = productPrice


class Cart:
    products = []
    totalPrice = 0

    def scan(self, raw):
        text = raw.decode("utf-8")
        id, name, price = text.split()
        isNewProduct = self.verifyProduct(id)
        product = Product(name, id, price)
        if isNewProduct:
            self.addProductToCart(product)
        else:
            self.removeProductFromCart(product)
        for product in self.products:
            print(product.name)

    def addProductToCart(self, product):
        self.products.append(product)
        self.totalPrice += int(product.price)
        print('The product: ' + product.name + 'was added to cart. Product price: ' + product.price)
        print('Total price so far: ' + str(self.totalPrice))

    def removeProductFromCart(self, product):
        self.remove(product.code)
        self.totalPrice -= int(product.price)
        print(product.name + ' was removed from the shopping cart')
        print('Total price so fat: ' + str(self.totalPrice))

    # iteram peste lista de produse -> daca gasim un produs cu id identic, il scoatem (asta inseamna ca nu-l vrem sa-l cumparam)
    def verifyProduct(self, id):
        # if len(self.products) == 0:
        # return True
        for product in self.products:
            if product.code == id:
                # print('Product code: '+ str(product.code) + ', id: ' + str(id))
                return False
        return True

    def remove(self, id):
        for product in self.products:
            if product.code == id:
                self.products.remove(product)
