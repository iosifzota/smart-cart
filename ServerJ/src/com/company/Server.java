package com.company;

import java.net.*;
import java.io.*;

public class Server {
    private ServerSocket serverSocket;
    private Socket clientSocket;
    private Socket readerSocket;
    private PrintWriter out;
    private BufferedReader in;

//    public void start(int port) throws IOException {
//        serverSocket = new ServerSocket(port);
//        clientSocket = serverSocket.accept();
////        out = new PrintWriter(clientSocket.getOutputStream(), true);
//        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
//        String inputLine = in.readLine();
////            out.println("hello client");
//
//    }

    public void start(int port) throws IOException {
        serverSocket = new ServerSocket(port);
        clientSocket = serverSocket.accept();
        Log.d("Server", "Connect with client");
        readerSocket = serverSocket.accept();
        //out = new PrintWriter(clientSocket.getOutputStream(), true);
        out = new PrintWriter(readerSocket.getOutputStream(), true);
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

        String inputLine;
        Log.d("Server", "Server Started");
        while ((inputLine = in.readLine()) != null) {
            if (".".equals(inputLine)) {
//                out.println("good bye");
                Log.d("Server", "Goodbye");
                break;
            }
            out.println(inputLine);
            //out.println(inputLine);
            Log.d("Server", "Read: " + inputLine);
        }
    }

    public void stop() throws IOException {
        in.close();
//        out.close();
        clientSocket.close();
        readerSocket.close();
        serverSocket.close();
    }
}

//public class Server {
//    private ServerSocket serverSocket = null;
//
//    public void start(int port) throws IOException {
//        if (null == serverSocket) {
//            serverSocket = new ServerSocket(port);
//            new EchoClientHandler(serverSocket.accept()).start();
//        } else {
//            Log.d("Server", "Server already started");
//        }
//    }
//
//    public void stop() throws IOException {
//        serverSocket.close();
//    }
//
//    private static class EchoClientHandler extends Thread {
//        private Socket clientSocket;
//        //private PrintWriter out;
//        private BufferedReader in;
//
//        public EchoClientHandler(Socket socket) {
//            this.clientSocket = socket;
//        }
//
//        public void run() {
//            try {
//                //out = new PrintWriter(clientSocket.getOutputStream(), true);
//
//                in = new BufferedReader(
//                        new InputStreamReader(clientSocket.getInputStream()));
//
//                String inputLine;
//                while ((inputLine = in.readLine()) != null) {
//                    if (".".equals(inputLine)) {
//                        //out.println("bye");
//                        break;
//                    }
//                    //out.println(inputLine);
//                    Log.d("Server", "Read: " + inputLine);
//                }
//
//                in.close();
//                //out.close();
//                clientSocket.close();
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//        }
//    }
//}
