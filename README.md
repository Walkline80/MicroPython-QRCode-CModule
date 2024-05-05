<h1 align="center">MicroPython QRCode CModule</h1>

<p align="center"><img src="https://img.shields.io/badge/Licence-MIT-green.svg?style=for-the-badge" /></p>

## 项目介绍

生成并显示指定内容的二维码

## 如何添加模块

> 以`ESP`系列芯片为例

* 在`MicroPython`项目同级目录克隆或粘贴本项目文件夹，并将文件夹重命名为`qrcode`

	```bash
	git clone https://gitee.com/walkline/micropython-qrcode-cmodule qrcode
	```

* 根据`MicroPython`项目固件编译说明做好前期准备

* 使用如下命令编译固件：

	```bash
	cd micropython/ports/esp32
	make USER_C_MODULES=../../../../qrcode/cmodules/micropython.cmake
	```

## 显示效果

| 控制台 | TFT | OLED |
| :-: | :-: | :-: |
| ![](./images/console.png) | ![](./images/tft.png) | ![](./images/oled.png) |

## 模块使用说明

参考项目目录下`tests`文件中的代码。

查看 [模块方法列表](./DOCS.md)

### 简单示例

生成二维码，并在控制台打印输出

```python
>>> import qrcode
>>> _qrcode = qrcode.QRCODE()
>>> _qrcode.ecc_level(qrcode.ECC_HIGH)
>>> _qrcode.generate('https://gitee.com/walkline/micropython-qrcode-cmodule')
I (66945) QRCODE_MODULE: Encoding below text with ECC LVL 3 & QR Code Version 40
I (66945) QRCODE_MODULE: https://gitee.com/walkline/micropython-qrcode-cmodule
>>> print(_qrcode)
<QRCODE version=6, max_version=40 length=41, ecc_level=3, buffer_size=210>
>>> _qrcode.print()
>>>
```

### 更多示例

```bash
# 使用 ab 工具烧录固件
$ ab --flash

# 使用 ab 工具上传相关文件
$ ab

# 使用 ab 工具打开串口
$ ab --repl

# 使用快捷键 ctrl+r，并选择以 _test 结尾的文件
```

## 参考资料

* [espressif/qrcode v0.1.0](https://components.espressif.com/components/espressif/qrcode)
* [MicroPython QRCode Research](https://gitee.com/walkline/micropython-qrcode-research)
* [AMPY Batch Tool](https://gitee.com/walkline/a-batch-tool)

## 合作交流

* 联系邮箱：<walkline@163.com>
* QQ 交流群：
	* 走线物联：[163271910](https://jq.qq.com/?_wv=1027&k=xtPoHgwL)
	* 扇贝物联：[31324057](https://jq.qq.com/?_wv=1027&k=yp4FrpWh)

<p align="center"><img src="https://gitee.com/walkline/WeatherStation/raw/docs/images/qrcode_walkline.png" width="300px" alt="走线物联"><img src="https://gitee.com/walkline/WeatherStation/raw/docs/images/qrcode_bigiot.png" width="300px" alt="扇贝物联"></p>
