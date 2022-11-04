# Makefile

# defaults
SIM ?= icarus
COCOTB_HDL_TIMEPRECISION = 1ns
TOPLEVEL_LANG ?= verilog

# Gate Level Sim
ifneq ($(GL),true)
VERILOG_SOURCES = $(PWD)/tb.v $(PWD)/simon.v 
else
COMPILE_ARGS    += -DGL_TEST
COMPILE_ARGS    += -DFUNCTIONAL
COMPILE_ARGS    += -DUSE_POWER_PINS
COMPILE_ARGS    += -DSIM
COMPILE_ARGS    += -DUNIT_DELAY=#1
VERILOG_SOURCES += primitives/primitives.v
VERILOG_SOURCES += primitives/sky130_fd_sc_hd.v

VERILOG_SOURCES += $(PWD)/tb.v runs/wokwi/results/final/verilog/gl/fraserbc_simon.v
endif

TOPLEVEL = tb
MODULE = bench

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
