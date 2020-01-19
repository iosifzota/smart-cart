package com.iot.smartcart;

import android.telephony.gsm.GsmCellLocation;
import android.util.Log;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.util.Consumer;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {
    private Socket clientSocket;
    //    private PrintWriter out;
    private BufferedReader in;

    public void startConnection(String ip, int port) throws IOException {
        clientSocket = new Socket(ip, port);
//        out = new PrintWriter(clientSocket.getOutputStream(), true);
        Log.d("Client", "Connected ok!");
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
    }

    public String sendMessage(String msg) throws IOException {
//        out.println(msg);
        String resp = in.readLine();
        return resp;
    }

    public void recv() throws IOException {
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            if (".".equals(inputLine)) {
//                out.println("good bye");
                Log.d("Client", "Goodbye");
                break;
            }
//            out.println(inputLine);
            Log.d("Client", "Read: " + inputLine);
            Global.mainActivity.handleState(inputLine);
        }
    }

    public void stopConnection() throws IOException {
        in.close();
//        out.close();
        clientSocket.close();
    }
}