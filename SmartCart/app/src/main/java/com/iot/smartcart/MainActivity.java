package com.iot.smartcart;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    public List<Product> mCart;
    private ListView lstCart;
    private TextView txtSum;

    Client client = new Client();

    Handler handler = null;


    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (null != client) {
            try {
                client.stopConnection();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public void test() {
        Log.d("MainActivity", "Test");
    }

    public void addToCart(Product p) {
        if (mCart.contains(p)) {
            mCart.remove(p);
        } else {
            mCart.add(p);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Global.mainActivity = this;

        lstCart = (ListView) findViewById(R.id.listCart);
        txtSum = findViewById(R.id.textSum);

        mCart = new ArrayList<>();
        updateDisplay();

        handler = new Handler(Looper.getMainLooper()) {
            @Override
            public void handleMessage(@NonNull Message msg) {
                String smsg = (String) msg.obj;
                Log.d("MainActivity", "handling msg " + msg.toString());
                addToCart(Product.fromStr(smsg));
                updateDisplay();
                super.handleMessage(msg);
            }
        };

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Log.d("MainActivity", "Opending server:5556");
                    Log.d("MainActivity", "Opending server:5556");
                    Log.d("MainActivity", "Opending server:5556");
                    Log.d("MainActivity", "Opending server:5556");
                    Log.d("MainActivity", "Opending server:5556");
                    Log.d("MainActivity", "Opending server:5556");
                    client.startConnection("35.246.183.183", 5556);
                    Log.d("MainActivity", "Receiving.");
                    client.recv();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    public void handleState(String msg) {
        Message completeMessage = handler.obtainMessage(1,msg);
        completeMessage.sendToTarget();
    }

    @Override
    protected void onResume() {
        super.onResume();

    }

    private void updateDisplay() {
        // Set up an ArrayAdapter to convert likely places into TextViews to populate the ListView
        ArrayAdapter<Product> placesAdapter =
                new ArrayAdapter<Product>(this, android.R.layout.simple_list_item_1, mCart);
        lstCart.setAdapter(placesAdapter);
        //lstPlaces.setOnItemClickListener(listClickedHandler);
        int sum = 0;
        for (Product p : mCart) {
            sum += p.getPrice();
        }
        txtSum.setText(Integer.toString(sum));
    }
}
