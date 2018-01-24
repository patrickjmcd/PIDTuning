"""PID Tuning Functions."""
import argparse

TUNE_FOR = 'setpoint_change'
LOOP_TYPE = 'PID'

SCAN_TIME = 0.01
DELTA_PV = 0.045
DELTA_MV = 0.08333
HYSTERESIS = 0.0447

T0 = 0.0
T25 = 0.21
T75 = 0.63


def calculate_delta_percentage(delta_val, eu_min, eu_max):
    """Calculate the delta percentage given a value and min and max values."""
    return delta_val / (eu_max - eu_min)


def calculate_loop_gains(tune_for, loop_type, scan_time, delta_pv, delta_mv, hysteresis, t0, t25, t75, verbose=False):
    """Calculate the loop gains for a particular P, PI, or PID loop."""
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

    process_gain = delta_pv / delta_mv
    time_constant = 0.9 * (t75 - t25)
    dead_time = (t75 - t0) - 1.4 * time_constant + scan_time

    [Ap, Bp, Ai, Bi, Ad, Bd] = [0, 0, 0, 0, 0, 0]
    p_gain = 0.0
    i_gain = 0.0
    d_gain = 0.0

    if loop_type == "P":
        try:
            [Ap, Bp] = TUNING_CONSTANTS[tune_for][loop_type][0]
        except IndexError:
            print("Error! Cannot tune a P loop for setpoint change")
            exit()

    if loop_type == "PI":
        [Ap, Bp] = TUNING_CONSTANTS[tune_for][loop_type][0]
        [Ai, Bi] = TUNING_CONSTANTS[tune_for][loop_type][1]

    if loop_type == "PID":
        [Ap, Bp] = TUNING_CONSTANTS[tune_for][loop_type][0]
        [Ai, Bi] = TUNING_CONSTANTS[tune_for][loop_type][1]
        [Ad, Bd] = TUNING_CONSTANTS[tune_for][loop_type][2]
    try:
        p_gain = (Ap * (dead_time / time_constant) ** Bp) / process_gain
        i_gain = time_constant / (Ai * (dead_time / time_constant) ** Bi)
        d_gain = Ad * (dead_time / time_constant) ** Bd * time_constant
    except Exception as e:
        print(e)

    if verbose:
        print("CALCULATION PARAMETERS")
        print("==================")
        print("Time Constant: {}".format(time_constant))
        print("Dead Time: {}".format(dead_time))
        print("Process Gain: {}".format(process_gain))

    return [p_gain, i_gain, d_gain]


parser = argparse.ArgumentParser(description="A program to calculate loop tuning parameters")
parser.add_argument('--tune-for', default="setpoint_change", type=str, help="Either setpoint_change or load_change")
parser.add_argument('--loop-type', default="PID", type=str, help="P, PI, or PID")
parser.add_argument('--scan-time', default=SCAN_TIME, type=float, help="Controller Scan Time in Seconds")
parser.add_argument('--delta-pv', default=DELTA_PV, type=float, help="Normalized value of DELTA_PV (in percentage)")
parser.add_argument('--delta-mv', default=DELTA_MV, type=float, help="Normalized value of DELTA_MV (in percentage)")
parser.add_argument('--hysteresis', default=HYSTERESIS, type=float, help="Normalized value of hysteresis (in percentage)")
parser.add_argument('--t0', default=T0, type=float, help="Starting seconds (can be epoch time or 0)")
parser.add_argument('--t25', default=T25, type=float, help="Seconds for PV to reach 25 percent of setpoint (can be epoch time or relative to t0)")
parser.add_argument('--t75', default=T75, type=float, help="Seconds for PV to reach 75 percent of setpoint (can be epoch time or relative to t0)")
parser.add_argument('-v', '--verbose', action='store_true', help="Displays intermediate calculation values")
args = parser.parse_args()

if __name__ == '__main__':
    [P_gain, I_gain, D_gain] = calculate_loop_gains(tune_for=args.tune_for, loop_type=args.loop_type,
                                                    scan_time=args.scan_time, delta_pv=args.delta_pv,
                                                    delta_mv=args.delta_mv, hysteresis=args.hysteresis,
                                                    t0=args.t0, t25=args.t25, t75=args.t75, verbose=args.verbose)
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
