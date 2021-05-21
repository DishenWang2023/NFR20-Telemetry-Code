sensor_names = ["Index", "Time", "FL_VSS", "FR_VSS", "BL_VSS", "BR_VSS", "FL_BRK_TMP", "FR_BRK_TMP",
                "BL_BRK_TMP", "BR_BRK_TMP", "FL_SUS_POT", "FR_SUS_POT", "BL_SUS_POT", "BR_SUS_POT", "F_BRK_PRES", "B_BRK_PRES",
                "STEER_ANG", "TPS", "OIL_PRES", "OIL_TEMP", "COOL_TEMP", "MAP", "MAT", "NEUT",
                "LAMBDA1", "LAMBDA2", "ACCEL", "GYRO", "GPS"]

sensors = {
    'rpm': {
        'label': "RPM",
        'units': 'revolutions',
        'max_value': 0,
    },
    'lambdas': {
        'label': 'Lambdas',
        'units': 'celsius',
        'max_value': 930,
    },
    'brake_temperature': {
        'label': 'Brake Temperature',
        'units': 'celsius',
        'max_value': 800,
    },
    'shock_potentiometers': {
        'label': 'Shock Potentiometers',
        'units': '',
        'max_value': 0,
    },
    'brake_pressure': {
        'label': 'Brake Pressure',
        'units': 'psi',
        'max_value': 0,
    },
    'throttle_position': {
        'label': 'Throttle Position',
        'units': '',
        'max_value': 0,
    },
    'intake_manifold_air_pressure': {
        'label': 'Intake Manifold Air Pressure',
        'units': 'psi',
        'max_value': 0,
    },
    'intake_manifold_air_temperature': {
        'label': 'Intake Manifold Air Temperature',
        'units': 'celsius',
        'max_value': 0,
    },
    'oil_pressure': {
        'label': 'Oil Pressure',
        'units': 'psi',
        'max_value': 0,
    },
    'oil_temperature': {
        'label': 'Oil Temperature',
        'units': 'celsius',
        'max_value': 0,
    },
    'cam_angle': {
        'label': 'Camber Angle',
        'units': 'degrees',
        'max_value': 0,
    },
    'coolant_temperature': {
        'label': 'Coolant Temperature',
        'units': 'celsius',
        'max_value': 0,
    },
    'crank_angle': {
        'label': 'Crank Angle',
        'units': 'degrees',
        'max_value': 0,
    }
    # talk to Tara and finish the sensor list
}

padding = 4