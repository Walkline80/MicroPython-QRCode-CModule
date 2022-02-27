"""
The MIT License (MIT)
Copyright © 2022 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-qrcode-cmodule
"""
from machine import SPI, Pin
import utime
import st7789
import qrcode
from config import Config

text = 'https://gitee.com/walkline/micropython-qrcode-cmodule'


def timed_function(f, *args, **kwargs):
	myname = str(f).split(' ')[1]
	def new_func(*args, **kwargs):
		t = utime.ticks_us()
		result = f(*args, **kwargs)
		delta = utime.ticks_diff(utime.ticks_us(), t)
		print('Function {} | Time = {:6.3f}ms'.format(myname, delta/1000))
		return result
	return new_func

@timed_function
def initialize_display():
	spi = SPI(
		1,
		baudrate=40000000,
		polarity=1,
		sck=Pin(Config.Pins.SCL),
		mosi=Pin(Config.Pins.SDA)
	)

	display = st7789.ST7789(
		spi, 240, 240,
		reset=Pin(Config.Pins.RST, Pin.OUT),
		dc=Pin(Config.Pins.DC, Pin.OUT)
	)
	display.init()

	return display

@timed_function
def display_qrcode_origin():
	global _display, _qrcode

	if _qrcode.generate(text):
		_qrcode.print()
		print(_qrcode)

		buffer_array = bytearray(_qrcode.length()**2 * 2)
		qrcodebuffer = bytearray(((_qrcode.length() - 1) // 8 + 1) * _qrcode.length())
		_qrcode.buffer_data(qrcodebuffer)

		_display.map_bitarray_to_rgb565(
			qrcodebuffer,
			buffer_array,
			_qrcode.length(),
			st7789.WHITE, st7789.BLACK
		)

		center_x = (_display.width() - _qrcode.length()) // 2
		center_y = (_display.height() - _qrcode.length()) // 2

		_display.blit_buffer(
			buffer_array,
			center_x, center_y,
			_qrcode.length(),
			_qrcode.length()
		)

@timed_function
def display_qrcode_scales():
	global _display

	if _qrcode.generate(text):
		_qrcode.print()
		print(_qrcode)

		scales = 5
		center_x = (_display.width() - _qrcode.length() * scales) // 2
		center_y = (_display.height() - _qrcode.length() * scales) // 2

		for y, row in enumerate(_qrcode.raw_data()):
			for x, value in enumerate(row):
				if value:
					_display.fill_rect(x * scales + center_x, y * scales + center_y, scales, scales, st7789.WHITE)


if __name__ == '__main__':
	_display = initialize_display()

	_qrcode = qrcode.QRCODE()
	_qrcode.ecc_level(3)

	display_qrcode_scales()
	# display_qrcode_origin()
