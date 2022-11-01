`timescale 1ns/1ns
`default_nettype none

module fraserbc_simon (
	io_in,
	io_out
);

	input  wire [7:0] io_in;
	output wire [7:0] io_out;

	/* Instantiate main module */
	simon simon0 (
		.i_clk(io_in[0]),
		.i_shift(io_in[1]),
		.i_data(io_in[2:5]),
		.o_data(io_out[0:3])
	);

endmodule

module lfsr_z0(
	i_clk,
	i_rst,
	o_data
);

	input  wire i_clk;
	input  wire i_rst;
	output wire o_data;

	reg [4:0] r_lfsr;
	assign o_data = r_lfsr[0];

	always @(posedge i_clk)
		if(i_rst)
			r_lfsr <= 5'b00001;
		else begin
			r_lfsr[4] <= r_lfsr[3];
			r_lfsr[3] <= r_lfsr[2];
			r_lfsr[2] <= r_lfsr[4] ^ r_lfsr[1];
			r_lfsr[1] <= r_lfsr[0];
			r_lfsr[0] <= r_lfsr[4] ^ r_lfsr[0];
		end

endmodule

module simon (
	i_clk,
	i_shift,
	i_data,
	o_data
);

	input  wire       i_clk;
	input  wire       i_shift;
	input  wire [3:0] i_data;
	output wire [3:0] o_data;

	reg r_lfsr_rst;
	initial r_lfsr_rst = 0;
	lfsr_z0 lfsr0 (
		.i_clk(i_clk),
		.i_rst(i_shift),
		.o_data(o_data[0])
	);

endmodule