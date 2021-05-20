hp_sens = {
    'FL_VSS': {
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
    'ACCELX':{
        'label': 'Accelerometer X (Longitudinal)',
        'id': 'ACCELX',
        'units': 'Gs',
        'min_value': 0,
        'max_value': 16
    },
    'ACCELY':{
        'label': 'Accelerometer Y (Latitudinal)',
        'id': 'ACCELY',
        'units': 'Gs',
        'min_value': 0,
        'max_value': 16
    },
    'ACCELZ':{
        'label': 'Accelerometer Z (Normal)',
        'id': 'ACCELZ',
        'units': 'Gs',
        'min_value': 0,
        'max_value': 16
    }
}

mp_sens = {
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
        'min_value': -4*250,
        'max_value': 4*250,
    },
    'GYROY': {
        'label': 'Gyroscope Y (Pitch)',
        'id': 'GYROY',
        'units': 'degrees/s',
        'min_value': -4*250,
        'max_value': 4*250,
    },
    'GYROZ': {
        'label': 'Gyroscope Z (Yaw)',
        'id': 'GYROZ',
        'units': 'degrees/s',
        'min_value': -4*250,
        'max_value': 4*250,
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
    }
}

lp_sens = {
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
    }
}

s_sens = {
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
    }
}

testing_sensors = {
    'gps': {
        'label': 'GPS',
        'units': 'PSI',
        'max_value': 0,
    },
    'strain1': {
        'label': 'Strain Gauges 1',
        'units': 'PSI',
        'max_value': 0,
    },
    'ptube1': {
        'label': 'Pitot Tube 1',
        'units': 'Celsius',
        'max_value': 0,
    }
}

used_sensors_list = ['fl_vss', 'fr_vss', 'bl_vss', 'br_vss', 'fl_sus_pot', 'fr_sus_pot', 'bl_sus_pot', 'br_sus_pot',
                     'steer_ang', 'tps', 'oil_pres', 'oil_temp', 'map', 'mat', 'fl_brk_tmp', 'fr_brk_tmp', 'bl_brk_tmp',
                     'br_brk_tmp', 'f_brk_pres', 'b_brk_pres', 'cool_temp']

