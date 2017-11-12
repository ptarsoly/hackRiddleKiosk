#include <SPI.h>
#include <MFRC522.h>

#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

#define SS_PIN 10
#define RST_PIN 9

#define FINGER_RX 3
#define FINGER_TX 4

MFRC522 mfrc522(SS_PIN, RST_PIN);

SoftwareSerial mySerial(FINGER_RX, FINGER_TX);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

int getFingerprintIDez();

bool isValidNFC (byte& ID);

byte byteIn = 0x00;
byte NFCID = 0x00;
byte fingerID = 0x00;

void setup() {
  Serial.begin(9600);
  
  SPI.begin();
  mfrc522.PCD_Init();
  
  finger.begin(57600);
}

void loop() {
  
  if(Serial.available() > 0) {
    
    byteIn = Serial.read();
    //Serial.println(byteIn,BIN);
    NFCID = (0xF0 & byteIn) >> 4;
    
    fingerID = 0x0F & byteIn;
    NFCID = 0x0c;
    fingerID = 0;
    //Serial.print("Finger ID: ");
    //Serial.println(fingerID);
    if(fingerID > 3) {
      Serial.print("0");
      return;
    }

    switch(fingerID) {
      case 0:
        if(isValidNFC(NFCID) && (getFingerprintIDez() == 156)) {
          Serial.print("1");
        }
        else {
          Serial.print("0");
        }
        //156, Peter
        break;
      case 1:
        //100, Max
        if(isValidNFC(NFCID) && (getFingerprintIDez() == 100)) {
          Serial.print("1");
        }
        else {
          Serial.print("0");
        }
        break;
      case 2:
        //158, Skyler
        if(isValidNFC(NFCID) && (getFingerprintIDez() == 158)) {
          Serial.print("1");
        }
        else {
          Serial.print("0");
        }
        break;
      case 3:
        //101, Muntaser
        if(isValidNFC(NFCID) && (getFingerprintIDez() == 101)) {
          Serial.print("1");
        }
        else {
          Serial.print("0");
        }
        break;
      default:
        Serial.print("0");
        break;
    }
    
  }
  Serial.flush();
  
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }
  
  // OK converted!
  p = finger.fingerFastSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("Did not find a match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }   
  
  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID); 
  Serial.print(" with confidence of "); Serial.println(finger.confidence); 
}

// returns -1 if failed, otherwise returns ID #
int getFingerprintIDez() {
  uint8_t p;
  unsigned long printTimeDelay = 100;
  unsigned long printTime = millis();
  while(millis()-printTime < printTimeDelay) {
    p = finger.getImage();
  }
  
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;
  
  // found a match!
  //Serial.print("Found ID #"); Serial.print(finger.fingerID); 
  //Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID; 
}


// Max
int getFingerprintID_max() {
  uint8_t p = finger.getImage();
  //uint8_t
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;
  
  // found a match!
  //Serial.print("Found ID #"); Serial.print(finger.fingerID); 
  //Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID; 
}

bool isValidNFC (byte& ID) {
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    //Serial.println("Not Present");
    return false;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    //Serial.println("Not Working");
    return false;
  }

  if((mfrc522.uid.uidByte[0] & 0x0F) == ID) {
    //Serial.println("It worked?");
    return true;
  }
  else {
    //Serial.println("False NFC");
    return false;
  }

  //Serial.println("WTF");
  return false;
}

