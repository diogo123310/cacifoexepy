/*Door lock system code
 * https://srituhobby.com
 */
 

#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
String UID1 = "31 E2 0C 06";
String UID2 = "0A 3A 43 06";
byte lock = 0;


LiquidCrystal_I2C lcd(0x27, 16, 2);
MFRC522 rfid(SS_PIN, RST_PIN);


void setup() {
  Serial.begin(9600); 
  lcd.init();
  lcd.backlight();
  SPI.begin();
  rfid.PCD_Init();
  pinMode(2, INPUT);
pinMode(3, OUTPUT);
digitalWrite(3, 0);
}

void loop() {
    int pinValue = digitalRead (2);
    Serial.println(pinValue);
    lcd.clear();
    if (pinValue == 0) {
  lcd.setCursor(4, 0);
  lcd.print("Welcome!");
  lcd.setCursor(1, 1);
  lcd.print("Put your card");

  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  if ( ! rfid.PICC_ReadCardSerial())
    return;
    
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Scanning");
  Serial.print("NUID tag is :");
  String ID = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    lcd.print(".");
    ID.concat(String(rfid.uid.uidByte[i] < 0x10 ? " 0" : " "));
    ID.concat(String(rfid.uid.uidByte[i], HEX));
    delay(300);
  }
  ID.toUpperCase();

  /*if (ID.substring(1) == UID && lock == 0 ) {
    servo.write(70);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Door is locked");
    delay(1500);
    lcd.clear();
    lock = 1;
  } else */
  if (ID.substring(1) == UID1 || UID2 ) {
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Door is open");
    digitalWrite(3,1);
    delay(20);
    digitalWrite(3,0);
    delay(1500);
    lcd.clear();
  
  } /*else if (ID.substring(1) == UID1 || UID2 ){
    digitalWrite(3,1);
    delay(300);
    digitalWrite(3,0);
    
  }*/
  else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Wrong card!");
    delay(1500);
    lcd.clear();
  }
    }
 if (pinValue == 1) {
      
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Close the Door");
      delay(2000);
    }
}