//Using Common Anode 7 segment displays
#include <WiFi.h>
#include <HTTPClient.h>
#include "wifi_config.h" // ssid name and password are saved in this file.

void display(int n, int k);
void clearDisplay();

int seg1[7] = {2,4,5,18,19,21,22};     // display 1
int seg2[7] = {23,25,26,27,32,33,13};  // display 2


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

  for (int i = 0; i<7; i++)
  {
    pinMode(seg1[i],OUTPUT);
    pinMode(seg2[i],OUTPUT);
  }

  clearDisplay();
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
    //Display consists of 2 7-Segment displays, so displaying only 2 digits using Multiplexing.
    int ones = total%10;
    int tens = (total/10)%10;
    for(int t = 0; t < 50; t++) {

    display(0, tens);   // display 1
    delay(2);
    // clearDisplay();

    display(1, ones);   // display 2
    delay(2);
    // clearDisplay();
  }
}

void display(int n, int k)
{
  int* seg = (n == 0) ? seg1 : seg2;

  switch(k)
  {
    case 0:
      digitalWrite(seg[0],LOW);
      digitalWrite(seg[1],LOW);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],LOW);
      digitalWrite(seg[4],LOW);
      digitalWrite(seg[5],LOW);
      digitalWrite(seg[6],HIGH);
      break;

    case 1:
      digitalWrite(seg[0],HIGH);
      digitalWrite(seg[1],LOW);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],HIGH);
      digitalWrite(seg[4],HIGH);
      digitalWrite(seg[5],HIGH);
      digitalWrite(seg[6],HIGH);
      break;

    case 2:
      digitalWrite(seg[0],LOW);
      digitalWrite(seg[1],LOW);
      digitalWrite(seg[2],HIGH);
      digitalWrite(seg[3],LOW);
      digitalWrite(seg[4],LOW);
      digitalWrite(seg[5],HIGH);
      digitalWrite(seg[6],LOW);
      break;

    case 3:
      digitalWrite(seg[0],LOW);
      digitalWrite(seg[1],LOW);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],LOW);
      digitalWrite(seg[4],HIGH);
      digitalWrite(seg[5],HIGH);
      digitalWrite(seg[6],LOW);
      break;

    case 4:
      digitalWrite(seg[0],HIGH);
      digitalWrite(seg[1],LOW);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],HIGH);
      digitalWrite(seg[4],HIGH);
      digitalWrite(seg[5],LOW);
      digitalWrite(seg[6],LOW);
      break;

    case 5:
      digitalWrite(seg[0],LOW);
      digitalWrite(seg[1],HIGH);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],LOW);
      digitalWrite(seg[4],HIGH);
      digitalWrite(seg[5],LOW);
      digitalWrite(seg[6],LOW);
      break;

    case 6:
      digitalWrite(seg[0],LOW);
      digitalWrite(seg[1],HIGH);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],LOW);
      digitalWrite(seg[4],LOW);
      digitalWrite(seg[5],LOW);
      digitalWrite(seg[6],LOW);
      break;

    case 7:
      digitalWrite(seg[0],LOW);
      digitalWrite(seg[1],LOW);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],HIGH);
      digitalWrite(seg[4],HIGH);
      digitalWrite(seg[5],LOW);
      digitalWrite(seg[6],HIGH);
      break;

    case 8:
      for(int i=0;i<7;i++) digitalWrite(seg[i],LOW);
      break;

    case 9:
      digitalWrite(seg[0],LOW);
      digitalWrite(seg[1],LOW);
      digitalWrite(seg[2],LOW);
      digitalWrite(seg[3],LOW);
      digitalWrite(seg[4],HIGH);
      digitalWrite(seg[5],LOW);
      digitalWrite(seg[6],LOW);
      break;
  }
}

void clearDisplay() {
  for (int i = 0; i < 7; i++) {
    digitalWrite(seg1[i], HIGH);
    digitalWrite(seg2[i], HIGH);
  }
}