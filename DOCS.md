<h1 align="center">MicroPython QRCode CModule</h1>
<p align="center"><img src="https://img.shields.io/badge/Licence-MIT-green.svg?style=for-the-badge" /></p>

## QRCODE 类

示例用法：

```python
import qrcode
_qrcode = qrcode.QRCODE()
_qrcode.ecc_level(qrcode.ECC_HIGH)
_qrcode.generate('https://gitee.com/walkline/micropython-qrcode-cmodule')
I (66945) QRCODE_MODULE: Encoding below text with ECC LVL 3 & QR Code Version 40
I (66945) QRCODE_MODULE: https://gitee.com/walkline/micropython-qrcode-cmodule
print(_qrcode)
<QRCODE version=6, max_version=40 length=41, ecc_level=3, buffer_size=210>
_qrcode.print()
>>>
```

### 构造器

* **class qrcode.QRCODE()**

	构建`QRCODE`对象实例。

### 方法列表

* **QRCODE([ecc_level, max_version])**

	* `ecc_level`：容错等级，默认值`ECC_MED`
	* `max_version`：可生成二维码的最大版本号，默认值`VERSION_MAX`

	```python
	# 版本号对应缓存大小计算方法
	((version * 4 + 17) ** 2 + 7) // 8 + 1
	```

	> 适当降低最大版本号可以减少占用的缓存

* **QRCODE.ecc_level([level])**

	获取或设置容错等级

* **QRCODE.version()**

	获取已生成二维码的版本号。

	```python
	# 版本号计算方法
	(QRCODE.length() - 17) // 4
	```

* **QRCODE.length()**

	获取已生成二维码的边长。

* **QRCODE.generate(text)**

	使用指定字符串生成二维码。

* **QRCODE.print()**

	在控制台打印二维码预览图。

* **QRCODE.raw_data()**

	获取二维码点阵元组数据，形如：

	```python
	((1, 0, ...), (0, 1, ...), ...)
	```	

* **buffer_data(byetarray, format[, scales, color, bg_color])**

	将二维码数据以指定格式填充到数组，其中：

	* `bytearray`：已初始化大小的`byetarray`数组
	* `format`：数据格式
	* `scales`：放大倍数，默认值`1`
	* `color`：前景颜色，默认值`1`或`0xffff`
	* `bg_color`：背景颜色，默认值`0`或`0x0000`

	```python
	# bytearray 初始化长度计算方法：
	
	# FORMAT_MONO_HLSB 格式
	(QRCODE.length() * scales - 1) // 8 + 1) * (QRCODE.length() * scales)
	
	# FORMAT_RGB565 格式
	(QRCODE.length() * scales) ** 2 * 2
	```

### 常量列表

* **qrcode.ECC_LOW**

	`7%`容错率。

	> `qrcode.ECC_LOW`代表二维码内容缺失`7%`后仍可被正确识别，容错率与数据长度成正比，下同。

* **qrcode.ECC_MED**

	`15%`容错率。

* **qrcode.ECC_QUART**

	`25%`容错率。

* **qrcode.ECC_HIGH**

	`30%`容错率。

* **qrcode.VERSION_MIN**

	二维码支持的最低版本：`1`。

* **qrcode.VERSION_MAX**

	二维码支持的最高版本：`40`。

* **qrcode.FORMAT_MONO_HLSB**

	指定`buffer_data()`函数填充数组的方式，适用于`OLED`屏幕。

* **qrcode.FORMAT_RGB565**

	指定`buffer_data()`函数填充数组的方式，适用于`TFT`屏幕。

## 合作交流

* 联系邮箱：<walkline@163.com>
* QQ 交流群：
	* 走线物联：[163271910](https://jq.qq.com/?_wv=1027&k=xtPoHgwL)
	* 扇贝物联：[31324057](https://jq.qq.com/?_wv=1027&k=yp4FrpWh)

<p align="center"><img src="https://gitee.com/walkline/WeatherStation/raw/docs/images/qrcode_walkline.png" width="300px" alt="走线物联"><img src="https://gitee.com/walkline/WeatherStation/raw/docs/images/qrcode_bigiot.png" width="300px" alt="扇贝物联"></p>
