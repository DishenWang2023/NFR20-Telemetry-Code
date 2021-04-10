//Arduino UNO Xbee Test Code
#include <SoftwareSerial.h>
SoftwareSerial xbee(0,1);
// above arguments are the pins that the xbee shield connects to

int pingPong = 1;
const int listLen = 26;
float count = 0;

void setup() {
  //Serial.begin(9600);
  Serial.println("Arduino started sending bytes via xbee");

  xbee.begin(9600);
}

float rawSenData[listLen] = {100    , 10   , 10.2  , 10.23 , 200  , 20     , 20.3 , 20.34,
                             2000.5 , 0    , 1     , 20    , 300  , 400    , 5000 , 6    ,
                             70     , 800  , 9000  , 10.343, 10.422, 10.000, 10.00, 10.0 ,
                             -10    , 0};
int sigList[listLen] = {0, 0, 1, 2, 0, 0, 1, 2,
                        1, 1, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 3, 3, 3, 2, 1,
                        0, 1}; 
                        // multiplications for each sensor values turning float to short
                        
short shortSenData[listLen]; 
short id = -32767;

void loop() {
  count += 0.1;
  rawSenData[listLen-1] = count;
  for (int i= 0; i < listLen; i++){
    // does not round yet
    shortSenData[i] = short(rawSenData[i] * pow(10,sigList[i])); // may not need to use a list
    xbee.write(highByte(shortSenData[i]));
    xbee.write(lowByte(shortSenData[i]));
  }
  xbee.write(highByte(id));
  xbee.write(lowByte(id));
  //xbee.println();
  //Serial.println();
  if (count > 1000){
    count = 0;
  }

// Triggers LED on arduino
  if (pingPong == 0) {
    digitalWrite(13, LOW);
  }
  else {
    digitalWrite(13, HIGH);
  }
  pingPong = 1 - pingPong;
  delay(100);
}
