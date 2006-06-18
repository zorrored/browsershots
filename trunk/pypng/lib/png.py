#!/usr/bin/env python
# png.py - PNG encoder in pure Python
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
PNG encoder in pure Python

This is an implementation of a subset of the PNG specification at
http://www.w3.org/TR/2003/REC-PNG-20031110 in pure Python.

It currently supports encoding of PPM files or raw data with 24 bits
per pixel (RGB) into PNG, with a number of options.

This file can be used in two ways:

1. As a command-line utility to convert PNM files to PNG. The
   interface is similar to that of the pnmtopng program from the
   netpbm package. Try "python png.py --help" for usage information.

2. As a module that can be imported and that offers methods to write
   PNG files directly from your Python program. For help, try the
   following in your python interpreter:
   >>> import png
   >>> help(png)

Changelog (recent first):
2006-06-17 Reworked into a class. Performance improvements to the
           interlacing code by Nicko
2006-06-17 Alpha-channel, grey-scale, 16-bit/plane support and test
           suite added by Nicko van Someren <nicko@nicko.org>
2006-06-15 Scanline iterator interface to avoid storing the whole
           input data in memory
2006-06-09 Very simple prototype implementation
"""


__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'


import sys, zlib, struct, math
from array import array

def interleave_planes(ipixels, apixels, width, height, ipsize, apsize):
    """
    Return an array of pixels consisting of the ipsize bytes of data from each pixel in
    ipixels followed by the apsize bytes of data from each pixel in apixels, for an
    image of size width x height.
    """
    pixelcount = width * height
    newpsize = ipsize + apsize
    itotal = pixelcount * ipsize
    atotal = pixelcount * apsize
    newtotal = pixelcount * newpsize
    # print ("w=%s, h=%s, total=%s, ips=%s, aps=%s, nps=%s, itotal=%s, atotal=%s, ntotal=%s"
    #        % (width, height, pixelcount, ipsize, apsize, newpsize, itotal, atotal, newtotal))
    # Set up the output buffer
    out = array('B')
    # It's annoying that there is no cheap way to set the array size :-(
    out.extend(ipixels)
    out.extend(apixels)
    # Interleave in the pixel data
    for i in range(ipsize):
        out[i:newtotal:newpsize] = ipixels[i:itotal:ipsize]
    for i in range(apsize):
        out[i+ipsize:newtotal:newpsize] = apixels[i:atotal:apsize]
    return out

class PNG:
    def __init__(self, width, height, pixel_bytes=None, alpha_bytes=None,
                 interlaced=False, trans=None,
                 background=None, gamma=None, compression=None,
                 chunk_limit=2**20, greyscale=False, has_alpha=False,
                 bytespersample=1):
        """
        Create a PNG image from RGB data.

        Arguments:
        outfile - something with a write() method
        scanlines - iterator that returns scanlines from top to bottom
        width, height - size of the image in pixels
        interlaced - scanlines are interlaced with Adam7
        transparent - create a tRNS chunk
        compression - zlib compression level (0-9)

        Each scanline must be an array of bytes of length 3*width,
        containing the red, green, blue values for each pixel.

        If the interlaced parameter is set to True, the scanlines are
        expected to be interlaced with the Adam7 scheme. This is good for
        incremental display over a slow network connection, but it
        increases encoding time and memory use by an order of magnitude
        and output file size by a factor of 1.2 or so.

        The transparent parameter can be used to mark a color as
        transparent in the resulting image file. If specified, it must be
        a tuple with three integer values for red, green, blue.
        """

        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be greater than zero")
        if alpha_bytes and has_alpha:
            raise ValueError("Extra alpha-channel data must not be supplied if pixels already have alpha data")
        if (alpha_bytes or has_alpha) and trans is not None:
            raise ValueError("Transparent colour not allowed with alpha channel")
        if bytespersample < 1 or bytespersample > 2:
            raise ValueError("Bytes per sample must be 1 or 2")

        if trans is not None:
            if greyscale:
                if not (len(trans) == 1 and type(trans[0]) is int):
                    raise ValueError("Transparent greyscale must be a 1-tuple of an integer")
            else:
                if not (len(trans) == 3 and type(trans[0]) is int and type(trans[1]) is int and type(trans[2]) is int):
                    raise ValueError("Transparent colour must be a triple of integers")

        if background is not None:
            if greyscale:
                if not (len(background) == 1 and type(background[0]) is int):
                    raise ValueError("Background greyscale must be a 1-tuple of an integer")
            else:
                if not (len(background) == 3 and type(background[0]) is int and
                        type(background[1]) is int and type(background[2]) is int):
                    raise ValueError("Background colour must be a triple of integers")

        if interlaced:
            self.interlaced = 1
        else:
            self.interlaced = 0

        self.pixel_bytes = pixel_bytes
        self.alpha_bytes = alpha_bytes

        self.width = width
        self.height = height
        self.interlaced = interlaced
        self.transparent = trans
        self.background = background
        self.gamma = gamma
        self.compression = compression
        self.chunk_limit = chunk_limit
        self.greyscale = greyscale
        self.has_alpha = has_alpha
        self.bytespersample = bytespersample

    def set_type_and_psize(self, with_alpha):
        if self.greyscale:
            self.colour_depth = 1
            if with_alpha:
                self.colour_type = 4
                self.psize = self.bytespersample * 2
            else:
                self.colour_type = 0
                self.psize = self.bytespersample
        else:
            self.colour_depth = 3
            if with_alpha:
                self.colour_type = 6
                self.psize = self.bytespersample * 4
            else:
                self.colour_type = 2
                self.psize = self.bytespersample * 3

    def write_chunk(self, outfile, tag, data):
        """
        Write a PNG chunk to the output file, including length and checksum.
        http://www.w3.org/TR/PNG/#5Chunk-layout
        """
        outfile.write(struct.pack("!I", len(data)))
        outfile.write(tag)
        outfile.write(data)
        checksum = zlib.crc32(tag)
        checksum = zlib.crc32(data, checksum)
        outfile.write(struct.pack("!I", checksum))

    def write(self, outfile):
        """
        Write out the pixel data in the PNG object as a PNG file
        """
        if not self.pixel_bytes:
            raise ValueError("No image data to write")
        self.write_array(outfile, self.pixel_bytes)

    def write_array(self, outfile, pdata):
        with_alpha = self.has_alpha or self.alpha_bytes
        self.set_type_and_psize(with_alpha)
        if self.alpha_bytes:
            ipsize = self.bytespersample * self.colour_depth
            pdata = interleave_planes(pdata, self.alpha_bytes, self.width, self.height, ipsize, self.bytespersample)
        if self.interlaced:
            scanlines = self.array_scanlines_interlace(pdata)
        else:
            scanlines = self.array_scanlines(pdata)
        self.write_image(outfile, scanlines)

    def convert_file(self, infile, outfile):
        """
        Convert the file infile contining raw pixel data into a PNG file outfile with the paramters set in the PNG object.
        """
        if self.interlace or self.alpha_bytes:
            pixels = array('B')
            pixels.fromfile(infile, self.bytespersample * self.colour_depth * self.width * self.height)
            self.write_array(outfile, pixels)
        else:
            scanlines = self.file_scanlines(infile)
            self.write_image(outfile, scanlines)

    def write_image(self, outfile, scanlines):
        # http://www.w3.org/TR/PNG/#5PNG-file-signature
        outfile.write(struct.pack("8B", 137, 80, 78, 71, 13, 10, 26, 10))

        # http://www.w3.org/TR/PNG/#11IHDR

        self.write_chunk(outfile, 'IHDR',
                         struct.pack("!2I5B", self.width, self.height, self.bytespersample * 8,
                                     self.colour_type, 0, 0, self.interlaced))

        # http://www.w3.org/TR/PNG/#11tRNS
        if self.transparent is not None:
            if self.greyscale:
                self.write_chunk(outfile, 'tRNS', struct.pack("!1H", *self.transparent))
            else:
                self.write_chunk(outfile, 'tRNS', struct.pack("!3H", *self.transparent))

        # http://www.w3.org/TR/PNG/#11bKGD
        if self.background is not None:
            if self.greyscale:
                self.write_chunk(outfile, 'bKGD', struct.pack("!1H", *self.background))
            else:
                self.write_chunk(outfile, 'bKGD', struct.pack("!3H", *self.background))

        # http://www.w3.org/TR/PNG/#11gAMA
        if self.gamma is not None:
            self.write_chunk(outfile, 'gAMA', struct.pack("!L", int(self.gamma * 100000)))

        # http://www.w3.org/TR/PNG/#11IDAT
        if self.compression is not None:
            compressor = zlib.compressobj(self.compression)
        else:
            compressor = zlib.compressobj()

        data = array('B')
        for scanline in scanlines:
            data.append(0)
            data.extend(scanline)
            if len(data) > self.chunk_limit:
                compressed = compressor.compress(data.tostring())
                if len(compressed):
                    # print >> sys.stderr, len(data), len(compressed)
                    self.write_chunk(outfile, 'IDAT', compressed)
                    data = array('B')
        if len(data):
            compressed = compressor.compress(data.tostring())
            flushed = compressor.flush()
            if len(compressed) or len(flushed):
                # print >> sys.stderr, len(data), len(compressed), len(flushed)
                self.write_chunk(outfile, 'IDAT', compressed + flushed)

        # http://www.w3.org/TR/PNG/#11IEND
        self.write_chunk(outfile, 'IEND', '')

    def file_scanlines(self, infile):
        """
        Generator for scanlines from an input file.
        """
        row_bytes = self.psize * self.width
        for y in range(self.height):
            scanline = array('B')
            scanline.fromfile(infile, row_bytes)
            yield scanline

    def array_scanlines(self, pixels):
        """
        Generator for scanlines from an array.
        """
        row_bytes = self.width * self.psize
        stop = 0
        for y in range(self.height):
            start = stop
            stop = start + row_bytes
            yield pixels[start:stop]

    def old_array_scanlines_interlace(self, pixels):
        """
        Generator for interlaced scanlines from an array.
        http://www.w3.org/TR/PNG/#8InterlaceMethods
        """
        adam7 = ((0, 0, 8, 8),
                 (4, 0, 8, 8),
                 (0, 4, 4, 8),
                 (2, 0, 4, 4),
                 (0, 2, 2, 4),
                 (1, 0, 2, 2),
                 (0, 1, 1, 2))
        row_bytes = self.psize * self.width
        for xstart, ystart, xstep, ystep in adam7:
            for y in range(ystart, self.height, ystep):
                if xstart < self.width:
                    if xstep == 1:
                        offset = y*row_bytes
                        yield pixels[offset:offset+row_bytes]
                    else:
                        row = array('B')
                        offset = y*row_bytes + xstart* self.psize
                        skip = self.psize * xstep
                        for x in range(xstart, self.width, xstep):
                            row.extend(pixels[offset:offset + self.psize])
                            offset += skip
                        yield row

    def array_scanlines_interlace(self, pixels):
        """
        Generator for interlaced scanlines from an array.
        http://www.w3.org/TR/PNG/#8InterlaceMethods
        """
        adam7 = ((0, 0, 8, 8),
                 (4, 0, 8, 8),
                 (0, 4, 4, 8),
                 (2, 0, 4, 4),
                 (0, 2, 2, 4),
                 (1, 0, 2, 2),
                 (0, 1, 1, 2))
        row_bytes = self.psize * self.width
        for xstart, ystart, xstep, ystep in adam7:
            for y in range(ystart, self.height, ystep):
                if xstart < self.width:
                    if xstep == 1:
                        offset = y*row_bytes
                        yield pixels[offset:offset+row_bytes]
                    else:
                        row = array('B')
                        # Note that we want the ceiling of (self.width - xstart) / xtep
                        row_len = self.psize * ((self.width - xstart + xstep - 1) / xstep)
                        # There's no easy way to set the length of an array other than extend
                        row.extend(pixels[0:row_len])
                        offset = y*row_bytes + xstart* self.psize
                        end_offset = (y+1) * row_bytes
                        skip = self.psize * xstep
                        for i in range(self.psize):
                            row[i:row_len:self.psize] = pixels[offset+i:end_offset:skip]
                        yield row

def read_pnm_header(infile, supported='P6'):
    """
    Read a PNM header, return width and height of the image in pixels.
    """
    header = []
    while len(header) < 4:
        line = infile.readline()
        sharp = line.find('#')
        if sharp > -1:
            line = line[:sharp]
        header.extend(line.split())
        if len(header) == 3 and header[0] == 'P4':
            break # PBM doesn't have maxval
    if header[0] not in supported:
        raise NotImplementedError('file format %s not supported' % header[0])
    if header[0] != 'P4' and header[3] != '255':
        raise NotImplementedError('maxval %s not supported' % header[3])
    return int(header[1]), int(header[2])

def pnmtopng(infile, outfile,
        interlace=None, transparent=None, background=None,
        gamma=None, compression=None):
    """
    Encode a PNM file into a PNG file.
    """
    width, height = read_pnm_header(infile)
    png = PNG(width, height,
              interlaced=interlace,
              transparent=transparent,
              background=background,
              gamma=gamma,
              compression=compression)
    png.convert_file(infile, outfile)


# FIXME: This needs to deal with deep colours and somewhere we need support for greyscale backgrounds etc.
def color_triple(color):
    """
    Convert a command line color value to a RGB triple of integers.
    """
    if color.startswith('#') and len(color) == 7:
        return (int(color[1:3], 16),
                int(color[3:5], 16),
                int(color[5:7], 16))


def _main():
    """
    Run the PNG encoder with options from the command line.
    """
    # Parse command line arguments
    from optparse import OptionParser
    version = '%prog ' + __revision__.strip('$').replace('Rev: ', 'r')
    parser = OptionParser(version=version)
    parser.set_usage("%prog [options] [pnmfile]")
    parser.add_option("--interlace", default=False, action="store_true",
                      help="create an interlaced PNG file (Adam7)")
    parser.add_option("--transparent",
                      action="store", type="string", metavar="color",
                      help="mark the specified color as transparent")
    parser.add_option("--background",
                      action="store", type="string", metavar="color",
                      help="store the specified background color")
    parser.add_option("--gamma",
                      action="store", type="float", metavar="value",
                      help="store the specified gamma value")
    parser.add_option("--compression",
                      action="store", type="int", metavar="level",
                      help="zlib compression level (0-9)")
    parser.add_option("--test", default=False, action="store_true",
                      help="run regression tests")
    parser.add_option("-R", "--test-red",
                      action="store", type="string", 
                      help="test patern for the red image layer")
    parser.add_option("-G", "--test-green",
                      action="store", type="string", 
                      help="test patern for the green image layer")
    parser.add_option("-B", "--test-blue",
                      action="store", type="string", 
                      help="test patern for the blue image layer")
    parser.add_option("-A", "--test-alpha",
                      action="store", type="string", 
                      help="test patern for the alpha image layer")
    parser.add_option("-D", "--test-deep",
                      default = False, action="store_true",
                      help="make test patern 16 bit per layer deep")
    parser.add_option("-S", "--test-size",
                      action="store", type="int",
                      help="linear size of the test image")

    (options, args) = parser.parse_args()
    # Convert options
    if options.transparent is not None:
        options.transparent = color_triple(options.transparent)
    if options.background is not None:
        options.background = color_triple(options.background)

    # Run regression tests
    if options.test:
        return test_suite(options)
    # Prepare input and output files
    if len(args) == 0:
        infile = sys.stdin
    elif len(args) == 1:
        infile = open(args[0], 'rb')
    else:
        parser.error("more than one input file")
    outfile = sys.stdout
    # Encode PNM to PNG
    pnmtopng(infile, outfile,
             interlace=options.interlace,
             transparent=options.transparent,
             background=options.background,
             gamma=options.gamma,
             compression=options.compression)


def test_suite(options):
    """
    Run regression tests and produce PNG files in current directory.
    """
# Below is a big stack of test image generators

    def _test_gradient_horizontal_lr(x, y):
        return x

    def _test_gradient_horizontal_rl(x, y):
        return 1-x

    def _test_gradient_vertical_tb(x, y):
        return y

    def _test_gradient_vertical_bt(x, y):
        return 1-y

    def _test_radial_tl(x, y):
        return max(1-math.sqrt(x*x+y*y), 0.0)

    def _test_radial_center(x, y):
        return _test_radial_tl(x-0.5, y-0.5)

    def _test_radial_tr(x, y):
        return _test_radial_tl(1-x, y)

    def _test_radial_bl(x, y):
        return _test_radial_tl(x, 1-y)

    def _test_radial_br(x, y):
        return _test_radial_tl(1-x, 1-y)

    def _test_stripe(x,n):
        return 1.0*(int(x*n) & 1)

    def _test_stripe_h_2(x, y):
        return _test_stripe(x, 2)

    def _test_stripe_h_4(x, y):
        return _test_stripe(x, 4)

    def _test_stripe_h_10(x, y):
        return _test_stripe(x, 10)

    def _test_stripe_v_2(x, y):
        return _test_stripe(y, 2)

    def _test_stripe_v_4(x, y):
        return _test_stripe(y, 4)

    def _test_stripe_v_10(x, y):
        return _test_stripe(y, 10)

    def _test_stripe_lr_10(x, y):
        return _test_stripe(x+y, 10)

    def _test_stripe_rl_10(x, y):
        return _test_stripe(x-y, 10)

    def _test_checker(x, y,n):
        return 1.0*((int(x*n) & 1) ^ (int(y*n) & 1))

    def _test_checker_8(x, y):
        return _test_checker(x, y, 8)

    def _test_checker_15(x, y):
        return _test_checker(x, y, 15)


    _test_patterns = {
        "GLR" : _test_gradient_horizontal_lr,
        "GRL" : _test_gradient_horizontal_rl,
        "GTB" : _test_gradient_vertical_tb,
        "GBT" : _test_gradient_vertical_bt,
        "RTL" : _test_radial_tl,
        "RTR" : _test_radial_tr,
        "RBL" : _test_radial_bl,
        "RBR" : _test_radial_br,
        "RCTR" : _test_radial_center,
        "HS2" : _test_stripe_h_2,
        "HS4" : _test_stripe_h_4,
        "HS10" : _test_stripe_h_10,
        "VS2" : _test_stripe_v_2,
        "VS4" : _test_stripe_v_4,
        "VS10" : _test_stripe_v_10,
        "LRS" : _test_stripe_lr_10,
        "RLS" : _test_stripe_rl_10,
        "CK8" : _test_checker_8,
        "CK15" : _test_checker_15,
        }
    

    def _test_pattern(width, height, depth, pattern):
        a = array('B')
        fw = float(width)
        fh = float(height)
        pfun = _test_patterns[pattern]
        if depth == 1:
            for y in range(height):
                for x in range(width):
                    a.append(int(pfun(float(x)/fw,float(y)/fh) * 255))
        elif depth == 2:
            for y in range(height):
                for x in range(width):
                    v = int(pfun(float(x)/fw,float(y)/fh) * 65535)
                    a.append(v >> 8)
                    a.append(v & 0xff)
        return a

    def _write_test(fname, size=256, red="GTB", green="RCTR", blue="LRS", alpha=None, depth=1, file_options = {}):
        out = open(fname, "wb")
        r = _test_pattern(size, size, depth, red)
        g = _test_pattern(size, size, depth, green)
        b = _test_pattern(size, size, depth, blue)
        if alpha:
            a = _test_pattern(size, size, depth, alpha)
        i = interleave_planes(r, g, size, size, depth, depth)
        i = interleave_planes(i, b, size, size, 2 * depth, depth)
        if alpha:
            i = interleave_planes(i, a, size, size, 3 * depth, depth)
        p = PNG(size, size, i, has_alpha = (alpha is not None), bytespersample = depth, **file_options)
        p.write(out)

    # The body of test_suite() 
    kw = {}
    if options.test_red:
        kw["red"] = options.test_red
    if options.test_green:
        kw["green"] = options.test_green
    if options.test_blue:
        kw["blue"] = options.test_blue
    if options.test_alpha:
        kw["alpha"] = options.test_alpha
    if options.test_deep:
        kw["depth"] = 2
    if options.test_size:
        kw["size"] = options.test_size

    kw["file_options"] = dict(interlaced=options.interlace,
                              trans=options.transparent,
                              background=options.background,
                              gamma=options.gamma,
                              compression=options.compression)

    _write_test('mixed.png', **kw)
    return 0

if __name__ == '__main__':
    _main()

