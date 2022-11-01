# Makefile

# defaults
SIM ?= icarus
COCOTB_HDL_TIMEPRECISION = 1ns
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += $(PWD)/tb.v $(PWD)/simon.v
TOPLEVEL = tb
MODULE = bench

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
