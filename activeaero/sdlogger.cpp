// #include "sdlogger.h"

// void SDLogger::setup() {
//   Serial.print("Initializing SD card...");

//   if (!SD.begin(10)) {
//     Serial.println("Initialization failed!");
//     while (1);
//   }
//   Serial.println("initialization done.");

//   // open the file. note that only one file can be open at a time,
//   // so you have to close this one before opening another.
//   logFile = SD.open("logs.txt", FILE_WRITE);

//   // if the file opened okay, write to it:
//   if (logFile) {
//     Serial.print("Opened Log");
// }
// }

// bool SDLogger::write(std::string log) {
//     if (logFile) {
//         // logFile.println(toCharArray(log));
//         return true;
//     } else {
//         return false;
//     }
// }

// void SDLogger::close() {
//     logFile.close();
// }