"""
The MIT License (MIT)
Copyright © 2022 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-qrcode-cmodule
"""
from machine import SPI, Pin
import utime
import gc
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

		scales = 4
		scale_length = _qrcode.length() * scales
		buffer_array = bytearray(scale_length ** 2 * 2)
		qrcodebuffer = bytearray(((scale_length - 1) // 8 + 1) * scale_length)
		_qrcode.buffer_data(qrcodebuffer, qrcode.FORMAT_MONO_HLSB, scales)

		_display.map_bitarray_to_rgb565(
			qrcodebuffer,
			buffer_array,
			scale_length,
			st7789.WHITE, st7789.BLACK
		)

		center_x = (_display.width() - scale_length) // 2
		center_y = (_display.height() - scale_length) // 2

		_display.blit_buffer(
			buffer_array,
			center_x, center_y,
			scale_length,
			scale_length
		)

@timed_function
def display_qrcode_scales_1():
	'''
	直接生成指定倍数的图像，图像大小受内存限制
	'''
	global _display, _qrcode

	if _qrcode.generate(text):
		_qrcode.print()
		print(_qrcode)

		scales = min(_display.width(), _display.height()) // _qrcode.length()

		while True:
			if (_qrcode.length() * scales) ** 2 * 2 + 10_000 > gc.mem_free():
				scales -= 1
			else:
				break

		if scales < 1:
			scales = 1

		scale_length = _qrcode.length() * scales
		buffer_array = bytearray(scale_length ** 2 * 2)
		_qrcode.buffer_data(buffer_array, qrcode.FORMAT_RGB565, scales) # , st7789.YELLOW, st7789.WHITE)

		center_x = (_display.width() - scale_length) // 2
		center_y = (_display.height() - scale_length) // 2

		_display.blit_buffer(
			buffer_array,
			center_x, center_y,
			scale_length,
			scale_length
		)

		del buffer_array

@timed_function
def display_qrcode_scales_2():
	'''
	使用点阵数据进行缩放显示，不受内存大小限制
	'''
	global _display, _qrcode

	if _qrcode.generate(text):
		_qrcode.print()
		print(_qrcode)

		# 根据屏幕尺寸计算最大缩放倍数
		scales = min(_display.width(), _display.height()) // _qrcode.length()
		scale_length = _qrcode.length() * scales

		center_x = (_display.width() - scale_length) // 2
		center_y = (_display.height() - scale_length) // 2

		color = st7789.WHITE
		bg_color = st7789.BLACK

		fill_bg = False

		for y, row in enumerate(_qrcode.raw_data()):
			for x, value in enumerate(row):
				if value:
					_display.fill_rect(x * scales + center_x, y * scales + center_y, scales, scales, color)
				else:
					if fill_bg:
						_display.fill_rect(x * scales + center_x, y * scales + center_y, scales, scales, bg_color)


if __name__ == '__main__':
	_display = initialize_display()

	_qrcode = qrcode.QRCODE()
	_qrcode.ecc_level(1)

	display_qrcode_scales_1()
	# display_qrcode_scales_2()
	# display_qrcode_origin()

	gc.collect()
