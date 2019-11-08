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

STATUS = 'S'
VIOLATION = 'V'
NOTIFICATION_TYPES = (
    ()
)
