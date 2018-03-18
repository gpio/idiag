#define DUREE 3000    //ms
#define RESOLUTION  2  //echantillonage en ms
#define PRESSOSTAT 250 //echelle du capteur de pression pour 5V
#define PVALID 50      //pression validant la courbe en mode auto 
#define S_START 5      // course de dcy

#include <MsTimer2.h>


enum PinAssignments {
pinA = 2, //codeur A
pinB = 3, //codeur B
pinP = 0 //entree analogique
};

volatile int S = 0; //traitee dans l'interruption(volatile)
byte P; //pression
volatile int courbeS[DUREE/RESOLUTION];
volatile byte courbeP[DUREE/RESOLUTION];
volatile unsigned int t;

void setup() {
  pinMode(pinA, INPUT); //codeur lineaire
  pinMode(pinB, INPUT);
  digitalWrite(pinA, HIGH);  // pull-up resistance
  digitalWrite(pinB, HIGH);  // pull-up resistance


  attachInterrupt(0, mesureS, CHANGE); //interruption hard
  MsTimer2::set(RESOLUTION, mesure); // echantillonage

  t=0;
  Serial.begin(57600);
}


void loop() {
  if (S < S_START && t<=1 ) {
      MsTimer2::start(); // active Timer2     
  }
  if (t == DUREE/RESOLUTION){
    MsTimer2::stop();
    t =0;
    Serial.print("{\"S\":[");   
    for (int i=0; i <= (DUREE/RESOLUTION-2); i++){
      Serial.print(courbeS[i]);
      Serial.print(",");
    }
    Serial.print(courbeS[DUREE/RESOLUTION-1]);
    Serial.print("], \"P\":[");
    for (int i=0; i <= (DUREE/RESOLUTION-2); i++){
      Serial.print(courbeP[i]);
      Serial.print(",");
    }
    Serial.print(courbeP[DUREE/RESOLUTION-1]);   
    Serial.println("]}");
      
    
    
  
    S=0;
  }
  if (S < 0) {
    S = 0;
  }
 
}

/****************
//interruptions :
****************/
// mesure de la course
void mesureS() {
  S += (digitalRead(pinA) != digitalRead(pinB)) ? +1 : -1;
}

//mesure frequentielle
void mesure() {
  courbeP[t] = (byte) analogRead(pinP);
  courbeS[t] = S;
  t++;
}

