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

	fraserbc_simon simon0 (
		.io_in({2'b00,i_data,i_shift,i_clk}),
		.io_out({o_data})
	);

endmodule
