#ifndef TELEMETRY_H
#define TELEMETRY_H

#include <string>
#include <vector>
#include <map>

#include <Adafruit_BNO08x.h>

class Telemetry {
  private:
    std::vector<double> acceleration(64, 0);
    
    Adafruit_BNO08x bno08x();
    sh2_SensorValue_t ndofSensorValue;
  public:
    Telemetry();
    std::map<std::string,std::vector<double>> getTelemetry();
};

#endif