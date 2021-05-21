import sys

all_sensors = ['Time', 'FL_VSS', 'FR_VSS', 'BL_VSS', 'BR_VSS', 'FL_SUS_POT', 'FR_SUS_POT', 'BL_SUS_POT', 'BR_SUS_POT',
               'STEER_ANG', 'OIL_TEMP', 'OIL_PRES', 'MAP', 'MAT', 'TPS', 'FL_BRK_TMP', 'FR_BRK_TMP', 'BL_BRK_TMP',
               'BR_BRK_TMP', 'F_BRK_PRES', 'B_BRK_PRES', 'COOL_TEMP', 'ACCELX', 'ACCELY', 'ACCELZ', 'GYROX', 'GYROY',
               'GYROZ', 'MAGNETX', 'MAGNETY', 'MAGNETZ', 'NEUT', 'AVG_VSS', 'LAMBDA1', 'LAMBDA2']

all_xbee_sensors = ['FL_VSS', 'FR_VSS', 'BL_VSS', 'BR_VSS', 'FL_SUS_POT', 'FR_SUS_POT', 'BL_SUS_POT', 'BR_SUS_POT',
               'FL_BRK_TMP', 'FR_BRK_TMP', 'BL_BRK_TMP', 'BR_BRK_TMP', 'F_BRK_PRES', 'B_BRK_PRES', 'COOL_TEMP', 'STEER_ANG',
                'TPS', 'OIL_TEMP', 'OIL_PRES', 'MAP', 'MAT', 'NEUT', "LAMBDA1", "LAMBDA2", 'ACCELX', 'ACCELY',
                'ACCELZ', 'GYROX', 'GYROY', 'GYROZ', 'MAGNETX', 'MAGNETY', 'MAGNETZ']

tabs = ['High Priority Sensors', 'Medium Priority Sensors', 'Low Priority Sensors', 'Safety Sensors']
tab_values = [("tab_"+str(i)) for i in range(len(tabs))]

group1 = ['AVG_VSS', 'FL_VSS', 'FR_VSS', 'BL_VSS', 'BR_VSS', 'ACCELX', 'ACCELY', 'ACCELZ']
group2 = ['FL_SUS_POT', 'FR_SUS_POT', 'BL_SUS_POT', 'BR_SUS_POT', 'STEER_ANG', 'GYROX', 'GYROY', 'GYROZ', 'MAGNETX',
          'MAGNETY', 'MAGNETZ', 'LAMBDA1', 'LAMBDA2']
group3 = ['TPS', 'OIL_PRES', 'OIL_TEMP', 'MAP', 'MAT', 'NEUT']
group4 = ['FL_BRK_TMP', 'FR_BRK_TMP', 'BL_BRK_TMP', 'BR_BRK_TMP', 'F_BRK_PRES', 'B_BRK_PRES', 'COOL_TEMP']

groups = [group1, group2, group3, group4]

# This dictionary contains all the relevant sensor info (label, part identifier, min/max, and units)
# The tabs on the GUI can be changed by changing the name of the dictionary that contains the individual sensors
# Add more sensors to the GUI by creating a new sensor in the relevant grouping with all of the sensors info, make
# sure to also add the part identifier of the new sensor to the 'all_sensors' list.
sensors_info = {
    'AVG_VSS': {
        'label': 'Averaged Wheel Speed',
        'id': 'AVG_VSS',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'FL_VSS': {  # This name needs to be the same as the sensor id
        'label': "Front Left Wheel Speed",
        'id': 'FL_VSS',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'FR_VSS': {
        'label': 'Front Right Wheel Speed',
        'id': 'FR_VSS',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'BL_VSS': {
        'label': 'Back Left Wheel Speed',
        'id': 'BL_VSS',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'BR_VSS': {
        'label': 'Back Right Wheel Speed',
        'id': 'BR_VSS',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'ACCELX': {
        'label': 'Accelerometer X (Longitudinal)',
        'id': 'ACCELX',
        'units': 'Gs',
        'min_value': -16,
        'max_value': 16
    },
    'ACCELY': {
        'label': 'Accelerometer Y (Latitudinal)',
        'id': 'ACCELY',
        'units': 'Gs',
        'min_value': -16,
        'max_value': 16
    },
    'ACCELZ': {
        'label': 'Accelerometer Z (Normal)',
        'id': 'ACCELZ',
        'units': 'Gs',
        'min_value': -16,
        'max_value': 16
    },
    'FL_SUS_POT': {
        'label': 'Front Left Suspension Potentiometer',
        'id': 'FL_SUS_POT',
        'units': 'in.',
        'min_value': 0,
        'max_value': 6.5,
    },
    'FR_SUS_POT': {
        'label': 'Front Right Suspension Potentiometer',
        'units': 'in.',
        'id': 'FR_SUS_POT',
        'min_value': 0,
        'max_value': 6.5,
    },
    'BL_SUS_POT': {
        'label': 'Back Left Suspension Potentiometer',
        'id': 'BL_SUS_POT',
        'units': 'in.',
        'min_value': 0,
        'max_value': 6.5,
    },
    'BR_SUS_POT': {
        'label': 'Back Right Suspension Potentiometer',
        'id': 'BR_SUS_POT',
        'units': 'in.',
        'min_value': 0,
        'max_value': 6.5,
    },
    'STEER_ANG': {
        'label': 'Steering Angle',
        'id': 'STEER_ANG',
        'units': 'degrees',
        'min_value': -180,
        'max_value': 180,
    },
    'GYROX': {
        'label': 'Gyroscope X (Roll)',
        'id': 'GYROX',
        'units': 'degrees/s',
        'min_value': -8 * 250,
        'max_value': 8 * 250,
    },
    'GYROY': {
        'label': 'Gyroscope Y (Pitch)',
        'id': 'GYROY',
        'units': 'degrees/s',
        'min_value': -8 * 250,
        'max_value': 8 * 250,
    },
    'GYROZ': {
        'label': 'Gyroscope Z (Yaw)',
        'id': 'GYROZ',
        'units': 'degrees/s',
        'min_value': -8 * 250,
        'max_value': 8 * 250,
    },
    'MAGNETX': {
        'label': 'Magnetometer X',
        'id': 'MAGNETX',
        'units': 'Teslas',
        'min_value': -4800,
        'max_value': 4800,
    },
    'MAGNETY': {
        'label': 'Magnetometer Y',
        'id': 'MAGNETX',
        'units': 'Teslas',
        'min_value': -4800,
        'max_value': 4800,
    },
    'MAGNETZ': {
        'label': 'Magnetometer Z',
        'id': 'MAGNETX',
        'units': 'Teslas',
        'min_value': -4800,
        'max_value': 4800,
},
    'TPS': {
        'label': 'Throttle Position',
        'id': 'TPS',
        'units': '%',
        'min_value': 0,
        'max_value': 90,
    },
    'OIL_PRES': {
        'label': 'Oil Pressure',
        'id': 'OIL_PRES',
        'units': 'PSI',
        'min_value': 0,
        'max_value': 100,
    },
    'OIL_TEMP': {
        'label': 'Oil Temperature',
        'id': 'OIL_TEMP',
        'units': 'Fahrenheit',
        'min_value': -80,
        'max_value': 150,
    },
    'MAP': {
        'label': 'Intake Manifold Air Pressure',
        'id': 'MAP',
        'units': 'Pa',
        'min_value': 0,
        'max_value': 100,
    },
    'MAT': {
        'label': 'Intake Manifold Air Temperature',
        'id': 'MAT',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 100,
},
    'FL_BRK_TMP': {
        'label': 'Front Left Brake Temperature',
        'id': 'FL_BRK_TMP',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'FR_BRK_TMP': {
        'label': 'Front Right Brake Temperature',
        'id': 'FR_BRK_TMP',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'BL_BRK_TMP': {
        'label': 'Back Left Brake Temperature',
        'id': 'BL_BRK_TMP',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'BR_BRK_TMP': {
        'label': 'Back Right Brake Temperature',
        'id': 'BR_BRK_TMP',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'F_BRK_PRES': {
        'label': 'Front Brake Pressure',
        'id': 'F_BRK_PRES',
        'units': 'PSI',
        'min_value': 0,
        'max_value': 1000,
    },
    'B_BRK_PRES': {
        'label': 'Back Brake Pressure',
        'id': 'B_BRK_PRES',
        'units': 'PSI',
        'min_value': 0,
        'max_value': 1000,
    },
    'COOL_TEMP': {
        'label': 'Coolant Temperature',
        'id': 'COOL_TEMP',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 150,
    },
    'NEUT': {
        'label': 'Neutral',
        'id': 'NEUT',
        'units': '',
        'min_value': 0,
        'max_value': 1,
    },
    'LAMBDA1': {
        'label': 'Lambda 1 (exhaust ratio / oxygen sensor)',
        'id': 'LAMBDA1',
        'units': '',
        'min_value': 0,
        'max_value': 1000
    },
    'LAMBDA2': {
        'label': 'Lambda 2',
        'id': 'LAMBDA2',
        'units': '',
        'min_value': 0,
        'max_value': 1000
    },
}