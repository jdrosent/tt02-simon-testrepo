import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

import struct
import ctypes
import json

with open("test_data.json", "r") as tfile:
    test_data = json.load(tfile)

# Behavioural-Level Test
@cocotb.test()
async def test_bl(dut):
    await test_simon(dut, gl=False)

# Gate-Level Test
@cocotb.test()
async def test_bl(dut):
    await test_simon(dut, gl=True)

# Main Test
async def test_simon(dut):
    # Set values initially to 0
    dut.i_shift.value = 0
    dut.i_data.value = 0

    # DUT Clock
    cocotb.start_soon(Clock(dut.i_clk, 2, "ns").start())
    await ClockCycles(dut.i_clk, 2)
    
    # Shift in key and plaintext
    key = test_data["key"]
    plaintext = test_data["plaintext"]

    dut.i_shift.value = 1
    await ClockCycles(dut.i_clk, 1)

    for x in range(8):
        dut.i_data.value = (plaintext >> (4*x)) & 0x0F
        await ClockCycles(dut.i_clk, 1)

    for x in range(16):
        dut.i_data.value = (key >> (4*x)) & 0x0F
        await ClockCycles(dut.i_clk, 1)
    
    dut.i_shift.value = 0

    # Check that rounds and key expansions match expected
    keys = test_data["keys"]
    rounds = test_data["rounds"]
    print("Key (Python)      Key (Verilog)     Round (Python)  Round (Verilog)")
    print("------------------------------------------------------------------")
    for x in range(len(keys)-1):
        await ClockCycles(dut.i_clk, 1)

        dut_key = dut.simon0.r_key.value
        dut_round = dut.simon0.r_round.value

        print(f"{keys[x]:016x}  {dut_key.integer:016x}  {rounds[x]:08x}        {dut_round.integer:08x}")
        assert(dut_key == keys[x])
        assert(dut_round == rounds[x])

    # Shift out the ciphertext
    dut.i_shift.value = 1
    await ClockCycles(dut.i_clk, 1)

    dut_key = dut.simon0.r_key.value

    ciphertext = 0
    for x in range(8):
        ciphertext += dut.o_data.value << (4*x)
        await ClockCycles(dut.i_clk, 1)

    print(f"{keys[-1]:016x}  {dut_key.integer:016x}  {rounds[-1]:08x}        {ciphertext:08x}")

    assert(keys[-1] == dut_key.integer)
    assert(rounds[-1] == ciphertext)