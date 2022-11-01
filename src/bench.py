import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

import struct
import ctypes

@cocotb.test()
async def test_simon(dut):
    cocotb.start_soon(Clock(dut.i_clk, 2, "ns").start())
    await ClockCycles(dut.i_clk, 2)
    
    dut.i_shift.value = 1
    await ClockCycles(dut.i_clk, 1)
    dut.i_shift.value = 0

    await ClockCycles(dut.i_clk, 62)