
#include <ESP8266WiFi.h>
//#include <HTTPClient.h>

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <SPI.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>


#define TFT_CS        5
#define TFT_RST       17
#define TFT_DC        12
#define TFT_MOSI      13
#define TFT_SCLK      14

#define ONE_WIRE_BUS  4


#define DHTPIN        D2
#define DHTTYPE       DHT11

#define BTN_1         25
#define BTN_2         26
#define BTN_3         27

#define LED_PIN       19
#define PUMP_PIN      21

#define LEVEL_PIN     15

#define ADC_PIN       34

//#define WATER_LOW     1
//#define WATER_HIGH    0

//
//
//const char* ssid = "SchoolX_Student";
//const char* password = "StudStud";
//const char* ssid = "5G_DONSTU_M";
 //const char* password = "{@univer2019donstu}";

WiFiServer server(80);
String headerHTTP;

//const char* serverName = "localhost:5000/data/";
//const char* serverName = "http://172.20.10.6:80";
//const char* serverName = "https://httpbin.org/post";

//IPAddress local_IP(172,20,10,6);
//IPAddress gateway(172,20,10,6);
//IPAddress subnet(255, 255, 0, 0);


DHT dht(DHTPIN, DHTTYPE);

float waterTempC;
float airTempC, humi;
int light;
int waterLevel;
int LEDState;
int pumpState;
int btn1, btn2, btn3;
//int auto_mode = 1;

uint32_t sensorTimer, serverTimer, buttonTimer;

void setup() {
  Serial.begin(115200);
//  if (!WiFi.config(local_IP, gateway, subnet)) {
//   Serial.println("STA Failed to configure");
//  }

  dht.begin();

  //Light sensor init
  pinMode(LEVEL_PIN, INPUT);

  //Buttons init
  pinMode(BTN_1, INPUT_PULLUP);
  pinMode(BTN_2, INPUT_PULLUP);
  pinMode(BTN_3, INPUT_PULLUP);

  //Reley pins init
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH);
  WiFi.begin("iPhone (Sergey)", "1234512345");
  
  // attempts to connect to Wifi network
  int attemptsCount = 0;
  while ((WiFi.status() != WL_CONNECTED) & (attemptsCount < 10)) {
    delay(500);
    Serial.print(".");
    attemptsCount++;
  }
  //one more attempt to connect to Wifi network
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("IP: ");
    Serial.println(WiFi.localIP());
    server.begin();
  }
  //
  //humi = 0;
  //
}

void loop() {
  WiFiClient client = server.available(); 
  if(client){
    Serial.println("New Client."); // выводим сообщение
    String currentLine = "";
    while (client.connected()) { // цикл, пока есть соединение клиента
      if (client.available()) { // если от клиента поступают данные,
        char c = client.read(); // читаем байт, затем
        Serial.write(c); // выводим на экран
        headerHTTP += c;
        if (c == '\n') { // если байт является переводом строки
          // если пустая строка, мы получили два символа перевода строки
          // значит это конец HTTP-запроса, формируем ответ сервера:
          if (currentLine.length() == 0) {
            // HTTP заголовки начинаются с кода ответа (напр., HTTP / 1.1 200 OK)
            // и content-type, затем пустая строка:
            if (headerHTTP.indexOf("GET /sensor_data") >= 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/plain");
            client.println("Connection: close");
            client.println();
            client.println(String(airTempC) + "/"  +String(humi));
            }
            else {
              client.println("HTTP/1.1 200 OK");
              client.println("Connection: close");
              client.println();
            }

            if (headerHTTP.indexOf("GET /led/1") >= 0) {
              Serial.println("led on");
//               auto_mode = 0;
              LEDState = 1;
              digitalWrite(LED_PIN, LOW);
            } else if (headerHTTP.indexOf("GET /led/0") >= 0) {
//              auto_mode = 0;
              Serial.println("led off");
              LEDState = 0;
              digitalWrite(LED_PIN, HIGH);
            } else if (headerHTTP.indexOf("GET /pump/1") >= 0) {
              //if(waterLevel != WATER_LOW){
                Serial.println("pump on");
                pumpState = 1;
                digitalWrite(PUMP_PIN, LOW);
              //}
            } else if (headerHTTP.indexOf("GET /pump/0") >= 0) {
               Serial.println("pump off");
               pumpState = 0;
              digitalWrite(PUMP_PIN, HIGH);
            }

            
            // HTTP-ответ завершается пустой строкой
            client.println();
            break;
          } else { // если получили новую строку, очищаем currentLine
            currentLine = "";
          }
        } else if (c != '\r') { // Если получили что-то ещё кроме возврата строки,
          currentLine += c; // добавляем в конец currentLine
        }
      }
    }
    // Очистим переменную
    headerHTTP = "";
    // Закрываем соединение
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }

//  if ((millis() - buttonTimer) > 100) {
//    buttonTimer = millis();
//    if(digitalRead(BTN_2) == 0){
//    auto_mode = 1;  
//    }
//  }
  
  if ((millis() - sensorTimer) > 2000) {
    
    sensorTimer = millis();

    Serial.println("air temp C*: ");
    Serial.println(1);
    Serial.println("humudity: ");
    Serial.println(1);
      
//  if(auto_mode == 1){
//    if(light > 3500){
//      LEDState = 0;
//       digitalWrite(LED_PIN, HIGH);
//    }
//    else{
//      LEDState = 1;
//      digitalWrite(LED_PIN, LOW);
//    }
//  }
  }

//  if ((millis() - serverTimer) > 5000) {
//    serverTimer = millis();
//    //Check WiFi connection status
//    if (WiFi.status() == WL_CONNECTED) {
//      WiFiClient client;
//      HTTPClient http;
//
//      // Your Domain name with URL path or IP address with path
//      http.begin(client, serverName);
//
//      // If you need an HTTP request with a content type: application/json, use the following:
//      http.addHeader("Content-Type", "application/json");
//      int httpResponseCode = http.POST("{\"api_key\":\"tPmAT5Ab3j7F9\",\"sensor\":\"BME280\",\"value1\":\"24.25\",\"value2\":\"49.54\",\"value3\":\"1005.14\"}");
//
//      Serial.print("HTTP Response code: ");
//      Serial.println(httpResponseCode);
//
//      // Free resources
//      http.end();
//    }
//    else {
//      Serial.println("WiFi Disconnected");
//    }
//  }

}
