#include "telemetry.h"

Telemetry::Telemetry(): acceleration(64, 0) {
    while (!bno08x.begin_UART()) {}
}

void setReports() {
    // bno08x.enableReport(SH2_ACCELEROMETER);
    bno08x.enableReport(SH2_GYROSCOPE_CALIBRATED);
    bno08x.enableReport(SH2_MAGNETIC_FIELD_CALIBRATED);
    bno08x.enableReport(SH2_ROTATION_VECTOR);
}

void Telemetry::pollBNO() {
  if(!bno08x.getSensorEvent(&sensorValue)) {
    return;
  }
  
  switch (sensorValue.sensorId) {
    case SH2_ROTATION_VECTOR:
        lOrientation = sensorValue;
        break;
    case SH2_MAGNETIC_FIELD_CALIBRATED:
        lMagnetometer = sensorValue;
        break;
    case SH2_GYROSCOPE_CALIBRATED:
        lGyroscope = sensorValue;
        break;
}

}

std::map<std::string,std::vector<double>> Telemetry::getTelemetry() {
    std::map<std::string,std::vector<double>> telemetry;
    std::vector<double> acceleration;
    std::vector<double> gyroscope;
    std::vector<double> magnetometer;
    std::vector<double> orientation;
    std::vector<double> pressure;
    std::vector<double> temperature;
    std::vector<double> altitude;
    
    
    gyroscope.push_back(lGyroscope.un.gyroscope.x);
    gyroscope.push_back(lGyroscope.un.gyroscope.y);
    gyroscope.push_back(lGyroscope.un.gyroscope.z);

    magnetometer.push_back(lMagnetometer.un.magneticField.x);
    magnetometer.push_back(lMagnetometer.un.magneticField.y);
    magnetometer.push_back(lMagnetometer.un.magneticField.z);

    orientation.push_back(lOrientation.un.rotationVector.i);
    orientation.push_back(lOrientation.un.rotationVector.j);
    orientation.push_back(lOrientation.un.rotationVector.k);
    orientation.push_back(lOrientation.un.rotationVector.real);
    
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