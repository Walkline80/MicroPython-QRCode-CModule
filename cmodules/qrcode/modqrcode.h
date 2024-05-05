/*
 * Copyright © 2022 Walkline Wang (https://walkline.wang)
 * Gitee: https://gitee.com/walkline/micropython-qrcode-cmodule
 */
#include "py/obj.h"
#include "py/runtime.h"

#include <string.h>
#include <stdlib.h>

#include "qrcodegen.h"

#define FORMAT_MONO_HLSB    0 /* Monochrome (1-bit) color format, byte are horizontally mapped */
#define FORMAT_RGB565       1 /* Red Green Blue (16-bit, 5+6+5) color format */

#define ECC_LOW   qrcodegen_Ecc_LOW     /* QR Code Error Tolerance of 7% */
#define ECC_MED   qrcodegen_Ecc_MEDIUM    /* QR Code Error Tolerance of 15% */
#define ECC_QUART qrcodegen_Ecc_QUARTILE  /* QR Code Error Tolerance of 25% */
#define ECC_HIGH  qrcodegen_Ecc_HIGH   /* QR Code Error Tolerance of 30% */

#define VERSION_MIN qrcodegen_VERSION_MIN   /* 1 */
#define VERSION_MAX qrcodegen_VERSION_MAX   /* 40 */

#define BLACK   0x0000
#define WHITE   0xFFFF

#define RGB2BGR_565(color) ((color & 0xF800) >> 11) | (color & 0x07E0) | ((color & 0x001F) << 11)

typedef struct _qrcode_obj_t {
    mp_obj_base_t base;
    uint8_t *buffer;
    int buffer_size;
    int version;    /* qrcode version, range [1, 40] */
    int length;     /* qrcode length, range [21, 177] */
    int ecc_level;
    int max_version;
} qrcode_obj_t;

mp_obj_t qrcode_QRCODE_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);
