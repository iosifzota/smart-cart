package com.company;

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
        }
    }

    public void stopConnection() throws IOException {
        in.close();
//        out.close();
        clientSocket.close();
    }

    public static void main(String[] args) throws IOException {
        Client client = new Client();
        client.startConnection("35.246.183.183", 5556);
        client.recv();
    }
}