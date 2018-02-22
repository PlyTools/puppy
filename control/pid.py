"""This is a simple implementation of a Proportional-Integral-Derivative (PID) Controller in the Python Programming Language.
More information about PID Controller: http://en.wikipedia.org/wiki/PID_controller
"""
import time

class PID:
    """PID Controller
    """

    def __init__(self, P=0.2, I=0.0, D=0.0, set_point=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.set_point = set_point

        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min

    def update(self,current_value):
        """
        Calculate PID output value for given reference input and feedback
        """
        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error

        self.Integrator = self.Integrator + self.error
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min
        self.I_value = self.Integrator * self.Ki

        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        PID = self.P_value + self.I_value + self.D_value

        return PID

    def setConfig(self, Kp=0, Ki=0, Kd=0, set_point=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):
        """Kp means proportional gain. Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = Kp
        """Ki means integral gain. Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = Ki
        """Kd means derivative gain. Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = Kd

        self.set_point = set_point
        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min

    def getStatus(self):
        return self.error

if __name__ == "__main__":
    readings = [1, 3, 5, 7, 12, 15, 17, 19, 27, 24, 24, 26]
    x = PID(0.5, .1, 1.5)

    for reading in readings:
        current_pid = x.update(reading)
        # if you want to know something else, like the error, you do
        err = x.getStatus()
        print(current_pid, err)