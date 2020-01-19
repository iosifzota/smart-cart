package com.iot.smartcart;

import android.util.Log;

import java.util.Objects;

public class Product {
    private final int id;
    private final String name;
    private final int price;

    public Product(int id, String name, int price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }

    public static Product fromStr(String rawProdInfoStr) {
        String[] prodInfoArray = rawProdInfoStr.trim().split(" ");

        if (prodInfoArray.length != 3) {
            Log.d("Product", "Too much information.");
            throw new RuntimeException("Too much information.");
        }

        try {
            int id = Integer.parseInt(prodInfoArray[0]);
            String name = prodInfoArray[1];
            int price = Integer.parseInt(prodInfoArray[2]);

            return new Product(id, name, price);
        } catch (NumberFormatException e) {
            Log.d("Product", "Invalid number format.");
            throw e;
        }
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return id + " " + name + "\t" + price;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Product product = (Product) o;
        return id == product.id;
    }
}
