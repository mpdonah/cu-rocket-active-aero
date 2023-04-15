#ifndef TELEMETRY_H
#define TELEMETRY_H

#include <string>
#include <vector>
#include <map>

#include <Adafruit_BNO08x.h>

class Telemetry {
  private:
    double baseAltitude;

    std::vector<double> acceleration;

    sh2_SensorValue_t lOrientation;
    sh2_SensorValue_t lMagnetometer;
    sh2_SensorValue_t lGyroscope;

    
    Adafruit_BNO08x bno08x();
    sh2_SensorValue_t sensorValue;
  public:
    Telemetry();

    void pollBNO()
    std::map<std::string,std::vector<double>> getTelemetry();
};

#endif