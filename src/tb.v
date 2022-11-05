`timescale 1ns/1ns
`default_nettype none

module tb (
	i_clk,
	i_shift,
	i_data,
	o_data
);

	/* Generate VCD dump */
	initial begin
		$dumpfile ("tb.vcd");
		$dumpvars (0, tb);
		#1;
	end

	/* Module Interface */
	input  wire       i_clk;
	input  wire       i_shift;
	input  wire [3:0] i_data;
	output wire [3:0] o_data;

	`ifdef GL_TEST
	/* Gate-Level Sim */
	fraserbc_simon simon0 (
		.io_in({2'b00,i_data,i_shift,i_clk}),
		.io_out({o_data}),
		.vccd1(1'b1),
        .vssd1(1'b0)
	);
	`else
	/* Behavioural-Level Sim */
	simon simon0 (
		.i_clk(i_clk),
		.i_shift(i_shift),
		.i_data(i_data),
		.o_data(o_data)
	);
	`endif

endmodule
