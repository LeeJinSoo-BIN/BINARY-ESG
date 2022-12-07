package com.seat.esg.controller;

import org.springframework.stereotype.Controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.StandardCharsets;

@Controller
public class FlaskController {

    public String responseFromFlask(){
        String url = "http://192.168.0.13:5000/predict";
        String sb = "";
        try {
            HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
            System.out.println("연결 완료!!!");

            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));

            String line = null;

            while ((line = br.readLine()) != null) {
                sb = sb + line + "\n";
            }

            System.out.println("sb = " + sb);

            br.close();

        } catch (MalformedURLException e) {
            System.out.println("연결 실패!!!");
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return sb;
    }
}
