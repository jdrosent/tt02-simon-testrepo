# Makefile

# defaults
SIM ?= icarus
COCOTB_HDL_TIMEPRECISION = 1ns
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES = $(PWD)/simon.v $(PWD)/tb.v

yosys: VERILOG_SOURCES = $(PWD)/synth.v $(PWD)/tb.v
yosys: all

TOPLEVEL = tb
MODULE = bench

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim