#ifndef FLIGHTSTATUS_H
#define FLIGHTSTATUS_H

#include <deque>
#include <vector>
#include <algorithm>

enum Stage {
    ARMED,
    ASCENT,
    COAST,
    APOGEE,
    DESCENT,
    ONGROUND,
};

class FlightStatus {
  private:
    Stage flightStage;
    std::deque<double> altitudeDeque;

    double median(std::vector<double> vec);
    bool checkApogee();
  public:
    FlightStatus(double baseAltitude);
    void newTelemetry(double acceleration, double altitude);
    Stage getStage();
};

#endif