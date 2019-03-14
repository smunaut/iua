BOARD ?= icebreaker
PROJ = iua_$(BOARD)_top
PIN_DEF = ../impl/iua_$(BOARD)_pins.pcf
DEVICE = up5k
PACKAGE = sg48

ARACHNE = arachne-pnr
ARACHNE_ARGS =
NEXTPNR = nextpnr-ice40
NEXTPNR_ARGS =
ICEPACK = icepack
ICETIME = icetime
ICEPROG = iceprog

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

all: $(PROJ).bin $(TESTBENCHES)

%_tb: %_tb.v $(ICE40_LIBS) $(OBJS)
	iverilog -Wall -DSIM=1 -o $@ $(ICE40_LIBS) $(OBJS) $<

%.blif %.json: %.v $(OBJS)
	yosys -p 'read_verilog $(VERILOG_DEFINES) $< $(OBJS); synth_ice40 -dffe_min_ce_use 4 -relut -top $(PROJ) -blif $*.blif -json $*.json'

%.asc: $(PIN_DEF) %.json
	$(NEXTPNR) $(NEXTPNR_ARGS) --$(DEVICE) --package $(PACKAGE) --json $*.json --pcf $(PIN_DEF) --asc $@ --freq 50

%.bin: %.asc
	$(ICEPACK) $< $@

%.rpt: %.asc
	$(ICETIME) -d $(DEVICE) -mtr $@ $<

prog: $(PROJ).bin
	$(ICEPROG) $<

sudo-prog: $(PROJ).bin
	@echo 'Executing prog as root!!!'
	sudo $(ICEPROG) $<

clean:
	rm -f $(PROJ).blif $(PROJ).json $(PROJ).asc $(PROJ).rpt $(PROJ).bin $(TESTBENCHES) *.vcd

.SECONDARY:
.PHONY: all prog clean
