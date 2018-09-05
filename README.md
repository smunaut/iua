`iua`: ice40 USB Analyzer
=========================

This analyzer samples 2 FPGA IOs at a fast rate and transmits the data in
compressed form over a serial link to the host.

Target
------

The code included in this repository was designed to be run on an UPduino
with an external 10 MHz clock fed in, mainly because this is what I had
on-hand.

It should be very trivially portable to other ice40 UltraPlus boards, and
even to any ice40 providing you replace the FIFO to use EBRs instead of
SPRAMs.


sigrok support
--------------

The `iua` support for sigrok is availabel at <https://github.com/smunaut/libsigrok>.

It is then possible to add the USB signaling and USB protocol decoders.

Beware than sigrok can be memory hungry when you feed 100 Msps data for long
periods !!!



Compression format
------------------

Each byte has :

  * The lower 2 LSBs are the state of the IOs
  * The upper 6 MSBs are a repeat count that indicate how many samples
    that state lasted (0=1 cycle, 1=2 cycles, ...)

If the repeat count is 63 (max value), this indicates that the repeat
count is extended and that the next two bytes to follow are used to
encode it (little endian).

Note that because a state might last more than the encodable 65536
cycles, the same state might need to be send several times.

Only decompression is specified, a compression engine is free to use
sub-obtimal encoding, as long as the decompressed result is identical.


License
-------

All code is GPL-v3 licensed
