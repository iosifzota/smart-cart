#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import logging
from RPLCD.i2c import CharLCD
from client import Client
from connection import *

client = Client(host,port)

def convertToRaw(id,name,price):
    text = str(id) + " " + name + " " + str(price)
    return text.encode()

class Product:
        def __init__ (self, name, code, price):
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
        def price(self,productPrice):
                self._price = productPrice

class Cart:
        products = []
        totalPrice = 0
        
        def __init__(self, reader):
                self._reader = reader
                self._lcd = CharLCD('PCF8574', 0x27)
                
        def scan(self, continue_reading):
                try:
                        while continue_reading:
                                id, text = self._reader.read()
                                text = text.strip()
                                if(not self.checkIfItIsCard(text)):
                                        name, price = text.split()
                                        sendData = convertToRaw(id,name,price)
                                        client.send(sendData)
                                        isNewProduct = self.verifyProduct(id)
                                        product = Product(name, id, price)
                                        if isNewProduct:
                                                self.addProductToCart(product)
                                        else:
                                                self.removeProductFromCart(product)
                                else:
                                        print('Your shopping is over')
                                        print()
                                        if(input('Do you want to pay? (y/n)') is 'y'):
                                                self.payProducts(text)
                                                break
                                        else:
                                                print('Your shopping is continuing')
                                                continue
                                time.sleep(1.5)
                        print('End')
                finally:
                        GPIO.cleanup()

        def addProductToCart(self, product):
                self.products.append(product)
                self.totalPrice += int(product.price)
                print('The product: ' + product.name + 'was added to cart. Product price: ' + product.price)
                print('Total price so far: ' + str(self.totalPrice))
                self.writeToLCD(product.name + ' added')
                                       
        def removeProductFromCart(self, product):
                self.remove(product.code)
                self.totalPrice -= int(product.price)
                print(product.name + ' was removed from the shopping cart')
                print('Total price so far: ' + str(self.totalPrice))
                self.writeToLCD(product.name + ' removed')
                                
        #iteram peste lista de produse -> daca gasim un produs cu id identic, il scoatem                
        def verifyProduct(self, id):
                #if len(self.products) == 0:
                        #return True
                for product in self.products:
                        if product.code == id:
                                #print('Product code: '+ str(product.code) + ', id: ' + str(id))
                                return False
                return True
        
        def remove(self, id):
                for product in self.products:
                        if product.code == id:
                                self.products.remove(product)

        def writeToLCD(self, text):
                self._lcd.clear()
                self._lcd.write_string(text)
                self._lcd.cursor_pos = (1, 0)
                self._lcd.write_string('Total: ')
                self._lcd.write_string(str(self.totalPrice))

        def checkIfItIsCard(self,text):
                return str.isdigit(text)

        def payProducts(self,money):
                print('Thank you for shopping')
                #aici putem sa intrebam daca doreste sa faca plata
                money = int(money)
                money -= int(self.totalPrice)
                self._lcd.clear()
                self._lcd.write_string(str(money))
                print(str(money))


if __name__ == "__main__":
        reader = SimpleMFRC522()
        shoppingCart = Cart(reader)
        shoppingCart.scan(True)
