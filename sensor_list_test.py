hp_sens = {
    'fl_vss': {
        'label': "Front Left Wheel Speed",
        'id': 'fl_vss',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'fr_vss': {
        'label': 'Front Right Wheel Speed',
        'id': 'fr_vss',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'bl_vss': {
        'label': 'Back Left Wheel Speed',
        'id': 'bl_vss',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'br_vss': {
        'label': 'Back Right Wheel Speed',
        'id': 'br_vss',
        'units': 'MPH',
        'min_value': 0,
        'max_value': 100,
    },
    'accel':{
        'label': 'Accelerometer',
        'id': 'accel',
        'units': 'Gs',
        'min_value': 0,
        'max_value': 16
    }
}

mp_sens = {
    'fl_sus_pot': {
        'label': 'Front Left Suspension Potentiometer',
        'id': 'fl_sus_pot',
        'units': 'in.',
        'min_value': 0,
        'max_value': 6.5,
    },
    'fr_sus_pot': {
        'label': 'Front Right Suspension Potentiometer',
        'units': 'in.',
        'id': 'fr_sus_pot',
        'min_value': 0,
        'max_value': 6.5,
    },
    'bl_sus_pot': {
        'label': 'Back Left Suspension Potentiometer',
        'id': 'bl_sus_pot',
        'units': 'in.',
        'min_value': 0,
        'max_value': 6.5,
    },
    'br_sus_pot': {
        'label': 'Back Right Suspension Potentiometer',
        'id': 'br_sus_pot',
        'units': 'in.',
        'min_value': 0,
        'max_value': 6.5,
    },
    'steer_ang': {
        'label': 'Steering Angle',
        'id': 'steer_ang',
        'units': 'degrees',
        'min_value': -180,
        'max_value': 180,
    },
    'gyro': {
        'label': 'Gyroscope',
        'id': 'gyro',
        'units': 'degrees/s',
        'min_value': -4*250,
        'max_value': 4*250,
    }
}

lp_sens = {
    'tps': {
        'label': 'Throttle Position',
        'id': 'tps',
        'units': '%',
        'min_value': 0,
        'max_value': 90,
    },
    'oil_pres': {
        'label': 'Oil Pressure',
        'id': 'oil_pres',
        'units': 'PSI',
        'min_value': 0,
        'max_value': 100,
    },
    'oil_temp': {
        'label': 'Oil Temperature',
        'id': 'oil_temp',
        'units': 'Fahrenheit',
        'min_value': -80,
        'max_value': 150,
    },
    'map': {
        'label': 'Intake Manifold Air Pressure',
        'id': 'map',
        'units': 'Pa',
        'min_value': 0,
        'max_value': 100,
    },
    'mat': {
        'label': 'Intake Manifold Air Temperature',
        'id': 'mat',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 100,
    }
}

s_sens = {
    'fl_brk_tmp': {
        'label': 'Front Left Brake Temperature',
        'id': 'fl_brk_tmp',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'fr_brk_tmp': {
        'label': 'Front Right Brake Temperature',
        'id': 'fr_brk_tmp',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'bl_brk_tmp': {
        'label': 'Back Left Brake Temperature',
        'id': 'bl_brk_tmp',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'br_brk_tmp': {
        'label': 'Back Right Brake Temperature',
        'id': 'br_brk_tmp',
        'units': 'Celsius',
        'min_value': 0,
        'max_value': 800,
    },
    'f_brk_pres': {
        'label': 'Front Brake Pressure',
        'id': 'f_brk_pres',
        'units': 'PSI',
        'min_value': 0,
        'max_value': 1000,
    },
    'b_brk_pres': {
        'label': 'Back Brake Pressure',
        'id': 'b_brk_pres',
        'units': 'PSI',
        'min_value': 0,
        'max_value': 1000,
    },
    'cool_temp': {
        'label': 'Coolant Temperature',
        'id': 'cool_temp',
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

