#!/usr/bin/env python3

"""
Reference sample decompression utiity

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
	while True:
		cd = do_read(fh_in, 1, hex_in)
		if len(cd) == 0:
			break

		pc = cd[0] >> 2
		d  = cd[0] & 3

		if pc == 0x3f:
			cd = do_read(fh_in, 2, hex_in)
			pc = (cd[1] << 8) | cd[0]

		do_write(fh_out, (bytes([d]) * (pc+1)), hex_out)
