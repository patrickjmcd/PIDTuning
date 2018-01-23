"""PID Tuning Functions."""

TUNE_FOR = 'setpoint_change'
LOOP_TYPE = 'PID'

SCAN_TIME = 0.01
DELTA_PV = 0.045
DELTA_MV = 0.08333
HYSTERESIS = 0.0447

T0 = 0.0
T25 = 0.21
T75 = 0.63

TUNING_CONSTANTS = {
    "load_change": {
        "P": [[0.902, -0.985]],
        "PI": [[0.984, -0.986], [0.608, -0.707]],
        "PID": [[1.435, -0.921], [0.8787, -0.749], [0.482, 1.137]]
    },
    "setpoint_change": {
        "P": [],
        "PI": [[0.758, -0.861], [01020, -0.323]],
        "PID": [[1.086, -0.869], [0.740, -0.130], [0.348, 0.914]]
    }
}

PG = DELTA_PV / DELTA_MV
TC = 0.9 * (T75 - T25)
DT = (T75 - T0) - 1.4 * TC + SCAN_TIME

[Ap, Bp, Ai, Bi, Ad, Bd] = [0, 0, 0, 0, 0, 0]
P_gain = 0.0
I_gain = 0.0
D_gain = 0.0

if LOOP_TYPE == "P":
    try:
        [Ap, Bp] = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0]
    except KeyError:
        print("Cannot tune a P loop for setpoint change")
        exit()

if LOOP_TYPE == "PI":
    [Ap, Bp] = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0]
    [Ai, Bi] = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][1]

if LOOP_TYPE == "PID":
    [Ap, Bp] = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0]
    [Ai, Bi] = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][1]
    [Ad, Bd] = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][2]
try:
    P_gain = (Ap * (DT / TC) ** Bp) / PG
    I_gain = TC / (Ai * (DT / TC) ** Bi)
    D_gain = Ad * (DT / TC) ** Bd * TC
except Exception as e:
    print(e)

print("CALCULATION PARAMETERS")
print("==================")
print("Time Constant: {}".format(TC))
print("Dead Time: {}".format(DT))

print("\n\nStandard PID Units")
print("==================")
print("P: {}".format(P_gain))
print("I: {} sec/repeat".format(I_gain))
print("D: {} sec".format(D_gain))
print("\n\nRockwell PID Units")
print("==================")
print("P: {}".format(P_gain))
print("I: {} min/repeat".format(I_gain / 60.0))
print("D: {} min".format(D_gain / 60.0))
