#!/usr/bin/env python3

"""
Reference sample compression utiity

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import binascii
import sys


def do_read(fh, n, as_hex):
	if as_hex:
		d = fh.read(n*2)
		return binascii.a2b_hex(d)
	else:
		return fh.read(n)

def do_write(fh, d, as_hex):
	if as_hex:
		d = binascii.b2a_hex(d)
	return fh.write(d)


with open(sys.argv[1],'rb') as fh_in, open(sys.argv[2], 'wb') as fh_out:
	hex_in  = sys.argv[1].endswith('.hex')
	hex_out = sys.argv[2].endswith('.hex')
	pd = do_read(fh_in, 1, hex_in)
	pc = 0
	while True:
		d = do_read(fh_in, 1, hex_in)
		if len(d) == 0:
			break

		if (d != pd) or (pc == (1 << 16)-1):
			if pc > 62:
				do_write(fh_out, bytes([pd[0] | 0xfc]), hex_out)
				do_write(fh_out, bytes([
					(pc >>  0) & 0xff,
					(pc >>  8) & 0xff,
				]), hex_out)
			else:
				do_write(fh_out, bytes([pd[0] | (pc << 2)]), hex_out)
			pc = 0
		else:
			pc += 1

		pd = d
