#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4; // Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; // Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; // Time at which the last beat occurred

float beatsPerMinute;
int beatAvg;

bool controle = false;
bool checar = true;

void setup()
{
  Serial.begin(115200);
  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) // Use default I2C port, 400kHz speed
  {
    Serial.println("0");
    while (1);
  }
  else
    Serial.println("1");

  particleSensor.setup(); // Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); // Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); // Turn off Green LED
}

void loop()
{
  if (checar)
    Serial.println("1");

  if (Serial.available()) // se byte pronto para leitura
  {
    switch (Serial.read()) // verifica qual caracter recebido
    {
    case 'L': // recebeu 'L'
      if (Serial && !controle)
        controle = true; // liga leitura
      if (checar)
        checar = false;
      break;
    case 'D': // recebeu 'D'
      controle = false; // desliga leitura
      checar = true;
      break;
    case 'F': // recebeu 'F'
      if (controle)
        controle = false;
      checar = true;
      delay(1);
      Serial.end(); // Encerra porta
      break;
    }
  }

  if (controle)
  {
    long irValue = particleSensor.getIR();
    int GSR = analogRead(A0);
    if (checkForBeat(irValue) == true)
    {
      // We sensed a beat!
      long delta = millis() - lastBeat;
      lastBeat = millis();

      beatsPerMinute = 60 / (delta / 1000.0);

      if (beatsPerMinute < 255 && beatsPerMinute > 20)
      {
        rates[rateSpot++] = (byte)beatsPerMinute; // Store this reading in the array
        rateSpot %= RATE_SIZE; // Wrap variable

        // Take average of readings
        beatAvg = 0;
        for (byte x = 0; x < RATE_SIZE; x++)
          beatAvg += rates[x];
        beatAvg /= RATE_SIZE;
      }
    }

    Serial.print(irValue);
    Serial.print(",");
    Serial.print((int)beatsPerMinute);
    Serial.print(",");
    Serial.print(beatAvg);
    Serial.print(",");
    Serial.print(GSR); // GSR
    Serial.println();
  }
}
