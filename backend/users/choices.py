DRIVER = 'D'
OFFICIAL = 'O'
USER_TYPES = (
    (DRIVER, 'Driver'),
    (OFFICIAL, 'Official')
)

MALE = 'M'
FEMALE = 'F'
SEX = (
    (MALE, 'Male'),
    (FEMALE, 'Female')
)

EYEGLASS = 'A'
UPPER_LIMB = 'B'
LOWER_LIMB = 'C'
DAYLIGHT = 'D'
HERING = 'E'
CONDITION_CODES = (
    (EYEGLASS, 'Wear eyeglasses'),
    (UPPER_LIMB, 'Drive with special equipment for upper limbs'),
    (LOWER_LIMB, 'Drive with special equipment for lower limbs'),
    (DAYLIGHT, 'Daylight driving only'),
    (HERING, 'Should always be accompanied by a person without hearing impairment')
)

OP = 'O+'
ON = 'O-'
AP = 'A+'
AN = 'A-'
BP = 'B+'
BN = 'B-'
ABP = 'AB+'
ABN = 'AB-'
BLOOD_TYPES = (
    (OP, OP),
    (ON, ON),
    (AP, AP),
    (AN, AN),
    (BP, BP),
    (BN, BN),
    (ABP, ABP),
    (ABN, ABN)
)

COLLISION = 'CO'
CLAMPED = 'CL'
TOW = 'TO'
OK = 'OK'
STATUS_TYPES = (
    (COLLISION, 'Traffic Collision'),
    (CLAMPED, 'Clamped'),
    (TOW, 'Towed'),
    (OK, 'OK')
)

TOW_LIST = ('tow', 'Tow')
COLLISION_LIST = ('collision', 'Collision')
CLAMP_LIST = ('clamp', 'Clamp')
TRAFFIC_VIOLATION_LIST = ('speeding', 'illegal parking',
                          'illegal right turn', 'illegal left turn', 'no helment', 'no license')
STATUS_TYPES_LIST = ('collision', 'Collision', 'tow',
                     'Tow', 'clamp', 'Clamp')

STATUS = 'S'
VIOLATION = 'V'
NOTIFICATION_TYPES = (
    (STATUS, 'Status'),
    (VIOLATION, 'Violation')
)


def status_points_map(val):
    for t in TOW_LIST:
        if t in val:
            return 3

    for c in COLLISION_LIST:
        if c in val:
            return 2

    for c in CLAMP_LIST:
        if c in val:
            return 2

    for t in TRAFFIC_VIOLATION_LIST:
        if t in val:
            return 1

    return 0
