"""
The MIT License (MIT)
Copyright © 2022 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-qrcode-cmodule
"""
from machine import SoftI2C, Pin
from drivers.ssd1306 import SSD1306_I2C
import framebuf
import gc
import qrcode
from config import Config

text = 'https://gitee.com/walkline/micropython-qrcode-cmodule'


def timed_function(f, *args, **kwargs):
	import utime

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
	i2c = SoftI2C(scl=Pin(Config.Pins.SCL), sda=Pin(Config.Pins.SDA))
	slave_list = i2c.scan()

	if slave_list and len (slave_list) == 1:
		print(f'found i2c device, id: {slave_list}')
		return SSD1306_I2C(128, 64, i2c)

@timed_function
def display_qrcode_scales_1():
	'''
	直接生成指定倍数的图像，图像大小受内存限制
	'''
	global _display, _qrcode

	if _qrcode.generate(text):
		_qrcode.print()
		print(_qrcode)

		# 根据屏幕尺寸计算最大缩放倍数
		min_width = min(_display.width, _display.height)
		scales = min_width // _qrcode.length()

		# 使二维码尽量全屏显示
		if _qrcode.length() * (scales + 1) - min_width == 2:
			scales += 1

		scale_length = _qrcode.length() * scales
		buffer_array = bytearray(((scale_length - 1) // 8 + 1) * scale_length)
		_qrcode.buffer_data(buffer_array, qrcode.FORMAT_MONO_HLSB, scales)

		center_x = (_display.width - scale_length) // 2
		center_y = (_display.height - scale_length) // 2

		_display.blit(
			framebuf.FrameBuffer(buffer_array, scale_length, scale_length, framebuf.MONO_HLSB),
			center_x, center_y
		)
		_display.show()

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
		min_width = min(_display.width, _display.height)
		scales = min_width // _qrcode.length()

		# 使二维码尽量全屏显示
		if _qrcode.length() * (scales + 1) - min_width == 2:
			scales += 1

		scale_length = _qrcode.length() * scales
		center_x = (_display.width - scale_length) // 2
		center_y = (_display.height - scale_length) // 2

		for y, row in enumerate(_qrcode.raw_data()):
			for x, value in enumerate(row):
				if value:
					_display.fill_rect(x * scales + center_x, y * scales + center_y, scales, scales, 1)

		_display.show()


if __name__ == '__main__':
	_display = initialize_display()

	if _display:
		_qrcode = qrcode.QRCODE()
		_qrcode.ecc_level(1)

		display_qrcode_scales_1()
		# display_qrcode_scales_2()
	else:
		print('no i2c device found')

	gc.collect()
