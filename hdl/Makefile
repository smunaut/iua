#
# Simulation Makefile
#

ICE40_LIBS=$(shell yosys-config --datdir/ice40/cells_sim.v)

OBJS=\
	iua_core.v	\
	iua_fifo.v	\
	iua_phy.v	\
	iua_sysmgr.v	\
	iua_top.v	\
	uart_tx.v	\
	sim_spram.v

TESTBENCHES=\
	iua_top_tb

all: $(TESTBENCHES)

%_tb: %_tb.v $(ICE40_LIBS) $(OBJS)
	iverilog -Wall -DSIM=1 -o $@ $(ICE40_LIBS) $(OBJS) $<

clean:
	rm -f $(TESTBENCHES) *.vcd
