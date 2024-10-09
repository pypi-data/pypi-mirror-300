import numpy as np
from scipy.optimize import leastsq

class RotationTransformation:
    def __init__(self):
        pass

    def roll(self, inputMat, g):  # rotation around x axis (bank angle)
        rollMat = np.array([[1, 0, 0],
                            [0, np.cos(g), -np.sin(g)],
                            [0, np.sin(g), np.cos(g)]])
        return np.dot(inputMat, rollMat)

    def pitch(self, inputMat, b):  # rotation around y axis (elevation angle)
        pitchMat = np.array([[np.cos(b), 0, np.sin(b)],
                             [0, 1, 0],
                             [-np.sin(b), 0, np.cos(b)]])
        return np.dot(inputMat, pitchMat)

    def yaw(self, inputMat, a):  # rotation around z axis (heading angle)
        yawMat = np.array([[np.cos(a), -np.sin(a), 0],
                           [np.sin(a), np.cos(a), 0],
                           [0, 0, 1]])
        return np.dot(inputMat, yawMat)

    def extractAngles(self, mat):
        """Extracts roll, pitch, and yaw angles from a rotation matrix mat"""
        x = np.arctan2(mat[2, 1], mat[2, 2])
        y = np.arctan2(-mat[2, 0], np.sqrt(pow(mat[2, 1], 2) + pow(mat[2, 2], 2)))
        z = np.arctan2(mat[1, 0], mat[0, 0])
        return x, y, z

    def combineAngles(self, x, y, z, reflect_z=False):
        """Combines separate roll, pitch, and yaw angles into a single rotation matrix."""
        eye = np.identity(3)
        R = self.roll(
            self.pitch(
                self.yaw(eye, z), y), x)
        
        if reflect_z:
            reflection_matrix = np.array([[1, 0, 0],
                                          [0, 1, 0],
                                          [0, 0, -1]])
            R = R @ reflection_matrix
        return R

    def func(self, x, measured_pts, global_pts, reflect_z=False):
        """Defines an error function for the optimization, 
        which calculates the difference 
        between transformed global points and measured points."""
        R = self.combineAngles(x[2], x[1], x[0], reflect_z=reflect_z)
        origin = np.array([x[3], x[4], x[5]]).T
        scale = np.array([x[6], x[7], x[8]])  # scaling factors for x, y, z axes

        error_values = np.zeros(len(global_pts) * 3)
        for i in range(len(global_pts)):
            global_pt = global_pts[i, :].T
            measured_pt = measured_pts[i, :].T * scale
            global_pt_exp = R @ measured_pt + origin
            error_values[i * 3: (i + 1) * 3] = global_pt - global_pt_exp

        return error_values

    def avg_error(self, x, measured_pts, global_pts, reflect_z=False):
        """Calculates the total error for the optimization."""
        error_values = self.func(x, measured_pts, global_pts, reflect_z)
        
        # Calculate the L2 error for each point
        l2_errors = np.zeros(len(global_pts))
        for i in range(len(global_pts)):
            error_vector = error_values[i * 3: (i + 1) * 3]
            l2_errors[i] = np.linalg.norm(error_vector)
        
        # Calculate the average L2 error
        average_l2_error = np.mean(l2_errors)
        
        return average_l2_error

    def fit_params(self, measured_pts, global_pts):
        """Fits parameters to minimize the error defined in func"""
        x0 = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1])  # initial guess: (x, y, z, x_t, y_t, z_t, s_x, s_y, s_z)
    
        if len(measured_pts) <= 3 or len(global_pts) <= 3:
            raise ValueError("At least three points are required for optimization.")
        
        # Optimize without reflection
        res1 = leastsq(self.func, x0, args=(measured_pts, global_pts, False), maxfev=5000)
        avg_error1 = self.avg_error(res1[0], measured_pts, global_pts, False)

        # Optimize with reflection
        res2 = leastsq(self.func, x0, args=(measured_pts, global_pts, True), maxfev=5000)
        avg_error2 = self.avg_error(res2[0], measured_pts, global_pts, True)

        # Select the transformation with the smaller total error
        if avg_error1 < avg_error2:
            rez = res1[0]
            R = self.combineAngles(rez[2], rez[1], rez[0], reflect_z=False)
            avg_err = avg_error1
        else:
            rez = res2[0]
            R = self.combineAngles(rez[2], rez[1], rez[0], reflect_z=True)
            avg_err = avg_error1

        origin = rez[3:6]
        scale = rez[6:]
        return origin, R, scale, avg_err  # translation vector, rotation matrix, and scaling factors