import urllib
import os
import sense_hat


# Class containing utility methods for multiple other classes
class ClimateUtil:
    # Returns true if able to connect to google, otherwise false
    @staticmethod
    def checkConnection():
        # Attempt connection
        try:
            host = urllib.request.urlopen("https://www.google.com")
            # Since connection was successful, return True
            return True
        except:
            # Since connection failed, return False
            return False

    # Get calibrated temperature
    # Reference: Week 4 Sensehat calibration example
    @staticmethod
    def getCalibratedTemp(sense):
        # Start up pressure sensor as to avoid values of 0
        sense.get_temperature_from_pressure()
        # Get temperature from humidity and pressure
        htemp = sense.get_temperature_from_humidity()
        ptemp = sense.get_temperature_from_pressure()
        # Get CPU temperature
        res = os.popen("vcgencmd measure_temp").readline()
        temp_cpu = float(res.replace("temp=", "").replace("'C\n", ""))
        # Calculate calibrated temperature
        temp = (htemp + ptemp) / 2
        temp_calibrated = temp - ((temp_cpu - temp) / 1.5)
        # Return calibrated temperature
        return temp_calibrated
