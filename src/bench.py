import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

import struct
import ctypes
import json
import random

import simon

# Behavioural-Level Test
@cocotb.test()
async def test_bl(dut):
	await test_simon(dut, gl=False)

# Gate-Level Test
@cocotb.test()
async def test_gl(dut):
	await test_simon(dut, gl=True)

async def test_simon(dut, gl=False):
	# DUT Clock
	cocotb.start_soon(Clock(dut.i_clk, 2, "ns").start())
	await ClockCycles(dut.i_clk, 2)
	
	# Run test 12 times
	for x in range(64):
		test_data = simon.get_test_data(arg_random=True)

		await encrypt(dut, test_data, gl)

		# Random delay
		await ClockCycles(dut.i_clk, random.randint(0, 16))

# Main Test
async def encrypt(dut, test_data, gl):
	# Set values initially to 0
	dut.i_shift.value = 0
	dut.i_data.value = 0
	
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

	# Read key and round values from test data
	keys = test_data["keys"]
	rounds = test_data["rounds"]

	print(f"Key: {keys[0]:016x}")
	print(f"Plaintext: {rounds[0]:08x}")

	# Check round and key expansions match expected
	if not gl:
		print("Key (Python)      Key (Verilog)     Round (Python)  Round (Verilog)")
		print("------------------------------------------------------------------")
		for x in range(len(keys)-1):
			await ClockCycles(dut.i_clk, 1)

			dut_key = dut.simon0.r_key.value
			dut_round = dut.simon0.r_round.value

			print(f"{keys[x]:016x}  {dut_key.integer:016x}  {rounds[x]:08x}        {dut_round.integer:08x}")
			assert(dut_key == keys[x])
			assert(dut_round == rounds[x])
	else:
		await ClockCycles(dut.i_clk, len(keys)-1)

	# Shift out the ciphertext
	dut.i_shift.value = 1
	await ClockCycles(dut.i_clk, 1)

	if not gl:
		dut_key = dut.simon0.r_key.value

	ciphertext = 0
	for x in range(8):
		ciphertext += dut.o_data.value << (4*x)
		await ClockCycles(dut.i_clk, 1)

	if not gl:
		print(f"{keys[-1]:016x}  {dut_key.integer:016x}  {rounds[-1]:08x}        {ciphertext:08x}")
		assert(keys[-1] == dut_key.integer)
	else:
		print(f"{rounds[-1]:08x} {ciphertext:08x}")

	dut.i_shift.value = 0

	assert(rounds[-1] == ciphertext)
