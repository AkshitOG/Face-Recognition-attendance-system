//Using Common Anode 7 segment displays
#include <WiFi.h>
#include <HTTPClient.h>
#include "wifi_config.h" // ssid name and password are saved in this file.

void display(int n, int k);


void setup() {
  Serial.begin(115200); 

  WiFi.begin(ssid, password); //ssid, password defined inside wifi_config.h
  Serial.print("Connecting to Wifi: ");
  Serial.println(ssid);
  Serial.print("connecting");
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected");

  for (int i = 0; i<=13; i++)
  {
    pinMode(i,OUTPUT);
  }

}

int total = 0;
unsigned long lastfetch = 0;
void loop() {
  if (millis()-lastfetch > 5000) 
  {
    lastfetch = millis();
    if (WiFi.status() == WL_CONNECTED)
    {
      HTTPClient http;

      String url = String(SERVER_URL) + "/total"; //SERVER_URL from wifi_config.h, keeping the ip hidden

      http.begin(url);
      int servercode = http.GET();
      
      if (servercode == 200)
      {
        String total_str = http.getString();
        total = total_str.toInt();
      }
      http.end();
    }
  }
    //Display consists of 2 7-Segment displays, so displaying only 2 digits.
    int a = total%10;
    int b = (total/10)%10;
    
    display(0,a);
    delay(5); //avoiding flickering
    display(1, b);
    delay(5); //avoid filckering

}

void display(int n, int k)
{
  int i = 0;
  if (n == 1) i = 7; 
  switch(k)
  {
    case 1:
    digitalWrite(0 + i,HIGH);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,HIGH);
    digitalWrite(4 + i,HIGH);
    digitalWrite(5 + i,HIGH);
    digitalWrite(6 + i,HIGH);
    break;

    case 2:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,HIGH);
    digitalWrite(3 + i,LOW);
    digitalWrite(4 + i,LOW);
    digitalWrite(5 + i,HIGH);
    digitalWrite(6 + i,LOW);
    break;

    case 3:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,LOW);
    digitalWrite(4 + i,HIGH);
    digitalWrite(5 + i,HIGH);
    digitalWrite(6 + i,LOW);
    break;

    case 4:
    digitalWrite(0 + i,HIGH);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,HIGH);
    digitalWrite(4 + i,HIGH);
    digitalWrite(5 + i,LOW);
    digitalWrite(6 + i,LOW);
    break;

    case 5:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,HIGH);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,LOW);
    digitalWrite(4 + i,HIGH);
    digitalWrite(5 + i,LOW);
    digitalWrite(6 + i,LOW);
    break;

    case 6:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,HIGH);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,LOW);
    digitalWrite(4 + i,LOW);
    digitalWrite(5 + i,LOW);
    digitalWrite(6 + i,LOW);
    break;

    case 7:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,HIGH);
    digitalWrite(4 + i,HIGH);
    digitalWrite(5 + i,LOW);
    digitalWrite(6 + i,HIGH);
    break;

    case 8:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,LOW);
    digitalWrite(4 + i,LOW);
    digitalWrite(5 + i,LOW);
    digitalWrite(6 + i,LOW);
    break;

    case 9:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,LOW);
    digitalWrite(4 + i,HIGH);
    digitalWrite(5 + i,LOW);
    digitalWrite(6 + i,LOW);
    break;

    case 0:
    digitalWrite(0 + i,LOW);
    digitalWrite(1 + i,LOW);
    digitalWrite(2 + i,LOW);
    digitalWrite(3 + i,LOW);
    digitalWrite(4 + i,LOW);
    digitalWrite(5 + i,LOW);
    digitalWrite(6 + i,HIGH);
    break;
  }
}
