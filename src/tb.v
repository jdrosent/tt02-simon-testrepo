`timescale 1ns/1ns
`default_nettype none

module tb (
	i_clk,
	i_shift,
	i_data,
	o_data
);

	initial begin
		$dumpfile ("tb.vcd");
		$dumpvars (0, tb);
		#1;
	end

	input  wire       i_clk;
	input  wire       i_shift;
	input  wire [3:0] i_data;
	output wire [3:0] o_data;

	simon simon (
		.i_clk(i_clk),
		.i_shift(i_shift),
		.i_data(i_data),
		.o_data(o_data)
	);

endmodule
