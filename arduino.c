#include "DHT.h"
#include <DS3232RTC.h>
#include <PCD8544.h>
#include <SD.h>
#include <SPI.h>

File myFile;
#define DHTPIN 2

DHT dht(DHTPIN, DHT22);
DS3232RTC myRTC;
PCD8544 lcd;

void setup() {
  lcd.begin(84, 48);
  Serial.begin(115200);
  myRTC.begin();
  setSyncProvider(myRTC.get);
  dht.begin();
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.print("Initializing SD card...");
  if (!SD.begin(10)) {
    Serial.println("initialization failed!");
  }
}
void loop() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(dht.readTemperature());
  lcd.setCursor(0, 1);
  lcd.print(dht.readHumidity());
  lcd.setCursor(0, 2);
  lcd.print(hour());
  lcd.setCursor(20, 2);
  lcd.print(minute());
  lcd.setCursor(40, 2);
  lcd.print(second());

  if (minute() == 59) {
    myFile = SD.open("test.txt");
    myFile.print(year());
    myFile.print("-");
    myFile.print(month());
    myFile.print("-");
    myFile.print(day());
    myFile.print(" ");
    myFile.print(hour());
    myFile.print(" ");
    myFile.print(dht.readTemperature());
    myFile.print(" ");
    myFile.println(dht.readHumidity());
    myFile.close();
  }

  delay(1000);
}
