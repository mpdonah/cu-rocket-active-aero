#include "telemetry.h"

Telemetry::Telemetry() {
    while (!bno08x.begin_UART()) {}
}

void setReports() {
    bno08x.enableReport(SH2_ACCELEROMETER);
    bno08x.enableReport(SH2_GYROSCOPE);
    bno08x.enableReport(SH2_MAGNETOMETER);
    bno08x.enableReport(SH2_ROTATION_VECTOR);
}

std::map<std::string,std::vector<double>> Telemetry::getTelemetry() {
    std::map<std::string,std::vector<double>> telemetry;
    std::vector<double> acceleration;
    std::vector<double> gyroscope;
    std::vector<double> orientation;
    std::vector<double> pressure;
    std::vector<double> temperature;
    std::vector<double> altitude;

    bno08x.getSensorEvent(&sensorValue);
    
    gyroscope.push_back(sensorValue.un.gyroscope.)

    orientation.push_back(sensorValue.un.rotationVector.i);
    orientation.push_back(sensorValue.un.rotationVector.j);
    orientation.push_back(sensorValue.un.rotationVector.k);
    orientation.push_back(sensorValue.un.rotationVector.real);
    
    pressure.push_back(sensorValue.pressure);
    temperature.push_back(sensorValue.temperature);
    altitude.push_back(sensorValue.altitude);

    telemetry["acceleration"] = acceleration;
    telemetry["orientation"] = orientation;
    telemetry["pressure"] = pressure;
    telemetry["temperature"] = temperature;
    telemetry["altitude"] = altitude;

    return telemetry;
}