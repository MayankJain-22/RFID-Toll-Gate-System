#include <SPI.h> 
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 53   // SDA pin on Mega
#define RST_PIN 49  // RST pin
#define SERVO_PIN 6 // Servo motor connected to pin 6
#define IR_SENSOR_PIN 7 // ✅ IR sensor connected to pin 7
#define ACCESS_DELAY 3000
#define DENIED_DELAY 1000

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance
Servo myServo; // Create Servo object

void setup() {
    Serial.begin(9600);
    SPI.begin();
    mfrc522.PCD_Init(); // Initialize RFID module

    myServo.attach(SERVO_PIN);
    myServo.write(170); // Servo locked position

    pinMode(IR_SENSOR_PIN, INPUT); // ✅ Set IR sensor as input

    // Serial.println("RFID + IR Gate System Ready. Scan RFID to open the gate.");
}

void loop() {
    // Look for new RFID card
    if (!mfrc522.PICC_IsNewCardPresent()) {
        return;
    }
    
    // Select one of the cards
    if (!mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    // Read UID and send it to PC
    String tagID = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        tagID += String(mfrc522.uid.uidByte[i], HEX);
    }

    Serial.println(tagID);  // Send UID to PC
    delay(500);

    // Wait for response from Python script
    while (Serial.available()) {
        String response = Serial.readString();
        response.trim();

        if (response == "OPEN") {
            // ("✅ Authorized access - Opening gate");
            myServo.write(30); // Unlock gate
            delay(ACCESS_DELAY);

            // ✅ Modified: Wait until IR sensor detects the car passing
            // ("Waiting for vehicle to pass...");
            
            // **Step 1: Wait until the car enters the sensor range (LOW)**
            while (digitalRead(IR_SENSOR_PIN) == HIGH) { 
                // ("No car detected. Waiting...");
                delay(100); // Prevents fast looping
            }

            //("🚗 Car detected inside gate");

            // **Step 2: Now wait for the car to fully pass (IR goes HIGH again)**
            while (digitalRead(IR_SENSOR_PIN) == LOW) { 
                // ("Car still inside... Keeping gate open.");
                delay(100);
            }

            // ("🚗 Car has passed - Closing gate");
            myServo.write(170); // Lock back
        }
    }

    // Halt PICC (to allow next reading)
    mfrc522.PICC_HaltA();
}
