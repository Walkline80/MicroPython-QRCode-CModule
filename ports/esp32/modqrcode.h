#include "qrcode.h"
#include "qrcodegen.h"

#define FORMAT_MONO_HLSB 0  /* Monochrome (1-bit) color format, byte are horizontally mapped */
#define FORMAT_RGB565    1  /* Red Green Blue (16-bit, 5+6+5) color format */

#define ECC_LOW   ESP_QRCODE_ECC_LOW   	/* QR Code Error Tolerance of 7% */
#define ECC_MED	  ESP_QRCODE_ECC_MED    /* QR Code Error Tolerance of 15% */
#define ECC_QUART ESP_QRCODE_ECC_QUART  /* QR Code Error Tolerance of 25% */
#define ECC_HIGH  ESP_QRCODE_ECC_HIGH   /* QR Code Error Tolerance of 30% */

#define VERSION_MIN qrcodegen_VERSION_MIN   /* 1 */
#define VERSION_MAX qrcodegen_VERSION_MAX   /* 40 */

typedef struct _qrcode_QRCODE_obj_t {
    mp_obj_base_t base;

    uint8_t *buffer;
    int buffer_size;
    int version;    /* qrcode version, range [1, 40] */
    int length;     /* qrcode length, range [21, 177] */
    int ecc_level;
    int max_version;
} qrcode_QRCODE_obj_t;

mp_obj_t qrcode_QRCODE_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);