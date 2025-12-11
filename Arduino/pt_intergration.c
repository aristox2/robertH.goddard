// -- Pressure Transducer Integration

#include "Wire.h"
#include "math.h"
#include "stdint.h"
#include "string.h"
#include <Adafruit_HDC302x.h>
#include <Adafruit_ICM20649.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_MPRLS.h"
#include "RTClib.h"
#include <SD.h>
#include <SoftwareSerial.h>

// --- Constants ---
#define ANALOG_READ_RESOLUTION_BITS 14
#define BAUD_RATE 115200
#define SENSOR_DELAY_MS 1000
#define NOMINAL_TEMP_C 25.0
#define TEMP_COEFF_ZERO 0.0005
#define TEMP_COEFF_SENS 0.0005

// --- Pressure Transducer Struct ---
typedef struct {
  float V_LOW;
  float V_HI;
  float PRESSURE_RANGE;
  int AI_PIN;
} PRESSURE_TRANSDUCER;

PRESSURE_TRANSDUCER pt1 = {
  0.5,   // V_LOW
  4.5,   // V_HI
  1600,  // PRESSURE_RANGE in PSI
  A0     // AI_PIN
};

typedef struct {
  uint16_t raw;
  float voltage;
  float pressure_psi;
  float drift_psi;
} DATA;a

// --- I2C and Sensor Declarations ---
RTC_DS3231 rtc;
Adafruit_MPRLS mpr = Adafruit_MPRLS(-1, -1);
Adafruit_ICM20649 icm;
Adafruit_HDC302x hdc = Adafruit_HDC302x();
SoftwareSerial xbee(0, 1);
File myFile;

const int chipSelect = 10;
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

// --- Read Analog Pressure Transducer ---
DATA readData(PRESSURE_TRANSDUCER pt) {
  uint16_t raw = analogRead(pt.AI_PIN);
  float voltage = raw * (5.0 / pow(2, ANALOG_READ_RESOLUTION_BITS));
  float pressure_psi = pt.PRESSURE_RANGE * ((voltage - pt.V_LOW) / (pt.V_HI - pt.V_LOW));
  if (pressure_psi < 0) pressure_psi = 0;

  float temp_delta = 20.5 - NOMINAL_TEMP_C;
  float drift_psi = pt.PRESSURE_RANGE * (fabs(temp_delta) * (TEMP_COEFF_ZERO + TEMP_COEFF_SENS));

  return { raw, voltage, pressure_psi, drift_psi };
}

void setup() {
  Serial.begin(BAUD_RATE);
  xbee.begin(BAUD_RATE);
  analogReadResolution(ANALOG_READ_RESOLUTION_BITS);

  #ifndef ESP8266
    while (!Serial);
  #endif

  if (!hdc.begin(0x44, &Wire) || !icm.begin_I2C(0x69, &Wire) || !mpr.begin(0x18, &Wire) || !rtc.begin()) {
    Serial.println("Could not find one or more Sensors");
    while (1);
  }

  if (!SD.begin(chipSelect)) {
    Serial.println("SD init failed. Check card and wiring.");
    while (1);
  }

  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop() {
  DATA data_1 = readData(pt1);

  sensors_event_t accel, gyro, temp;
  icm.getEvent(&accel, &gyro, &temp);

  double temper = 0.0, RH = 0.0;
  hdc.readTemperatureHumidityOnDemand(temper, RH, TRIGGERMODE_LP0);

  float pressure_hPa = mpr.readPressure();
  DateTime now = rtc.now();

  char line[256];
  snprintf(line, sizeof(line),
    "Hour: %02i, Min: %02i, Sec: %02i, Analog_Pressure: %.2f PSI, Analog_Voltage: %.3f V, MPRLS_Pressure: %.2f hPa, AX: %.2f, AY: %.2f, AZ: %.2f, GX: %.2f, GY: %.2f, GZ: %.2f, Humidity: %.2f %%, Temp(C): %.2f",
    now.hour(), now.minute(), now.second(),
    data_1.pressure_psi, data_1.voltage, //You can pass the parameter by calling: "data_1." followed by a specific variable  
    pressure_hPa,
    accel.acceleration.x, accel.acceleration.y, accel.acceleration.z,
    gyro.gyro.x, gyro.gyro.y, gyro.gyro.z,
    RH, temper
  );

  while (xbee.available()) {
    char c = xbee.read();
    Serial.print("Received: ");
    Serial.println(c);
  }

  myFile = SD.open("myfile.csv", FILE_WRITE);
  if (myFile) {
    myFile.println(line);
    myFile.close();
    Serial.println("Line saved");
  } else {
    Serial.println("error opening myfile.csv");
  }

  xbee.println(line);
  Serial.println(line);

  delay(SENSOR_DELAY_MS);
}
