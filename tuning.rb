# PID Tuning Functions.

TUNE_FOR = 'setpoint_change'
LOOP_TYPE = 'PID'

SCAN_TIME = 0.01
DELTA_PV = 0.045
DELTA_MV = 0.08333
HYSTERESIS = 0.0447

t0 = 0.0
t25 = 0.21
t75 = 0.63

TUNING_CONSTANTS = {
    "load_change" => {
        "P" => [[0.902, -0.985]],
        "PI" => [[0.984, -0.986], [0.608, -0.707]],
        "PID" => [[1.435, -0.921], [0.8787, -0.749], [0.482, 1.137]]
    },
    "setpoint_change" => {
        "P" => [],
        "PI" => [[0.758, -0.861], [01020, -0.323]],
        "PID" => [[1.086, -0.869], [0.740, -0.130], [0.348, 0.914]]
    }
}

process_gain = DELTA_PV / DELTA_MV
time_constant = 0.9 * (t75 - t25)
dead_time = (t75 - t0) - 1.4 * time_constant + SCAN_TIME

a_p = 0.0
b_p = 0.0
a_i = 0.0
b_i = 0.0
a_d = 0.0
b_d = 0.0

p_gain = 0.0
i_gain = 0.0
d_gain = 0.0

if LOOP_TYPE == "P"
  begin
    a_p = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0][0]
    b_p = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0][1]
  rescue NoMethodError
    puts "ERROR! Cannot tune P-Only loop for setpoint change"
  end

elsif LOOP_TYPE == "PI"
  a_p = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0][0]
  b_p = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0][1]
  a_i = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][1][0]
  b_i = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][1][1]

elsif LOOP_TYPE == "PID"
  a_p = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0][0]
  b_p = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][0][1]
  a_i = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][1][0]
  b_i = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][1][1]
  a_d = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][2][0]
  b_d = TUNING_CONSTANTS[TUNE_FOR][LOOP_TYPE][2][1]
end

p_gain = (a_p * (dead_time / time_constant) ** b_p) / process_gain
i_gain = time_constant / (a_i * (dead_time / time_constant) ** b_i)
d_gain = a_d * (dead_time / time_constant) ** b_d * time_constant


puts "CALCULATION PARAMETERS"
puts "=================="
puts "Time Constant: #{time_constant}"
puts "Dead Time: #{dead_time}"

puts "\n\nStandard PID Units"
puts "=================="
puts "P: #{p_gain}"
puts "I: #{i_gain}"
puts "D: #{d_gain}"
puts "\n\nRockwell PID Units"
puts "=================="
puts "P: #{p_gain}"
puts "I: #{i_gain / 60.0} min/repeat"
puts "D: #{d_gain / 60.0} min"
