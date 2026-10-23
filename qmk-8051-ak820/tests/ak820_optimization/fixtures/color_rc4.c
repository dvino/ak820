/* GPL-2.0-or-later: RC4 HSV reference, commit cb9ff6ea. */
RGB rc4_hsv_to_rgb_impl(HSV hsv, bool use_cie) {
    RGB      rgb;
    uint8_t  region, remainder, p, q, t;
    uint16_t h, s, v;

    if (hsv.s == 0) {
#ifdef USE_CIE1931_CURVE
        if (use_cie) {
            rgb.r = rgb.g = rgb.b = pgm_read_byte(&CIE1931_CURVE[hsv.v]);
        } else {
            rgb.r = hsv.v;
            rgb.g = hsv.v;
            rgb.b = hsv.v;
        }
#else
        rgb.r = hsv.v;
        rgb.g = hsv.v;
        rgb.b = hsv.v;
#endif
        return rgb;
    }

    h = hsv.h;
    s = hsv.s;
#ifdef USE_CIE1931_CURVE
    if (use_cie) {
        v = pgm_read_byte(&CIE1931_CURVE[hsv.v]);
    } else {
        v = hsv.v;
    }
#else
    v = hsv.v;
#endif

    region    = h * 6 / 255;
    remainder = (h * 2 - region * 85) * 3;

    p = (v * (255 - s)) >> 8;
    q = (v * (255 - ((s * remainder) >> 8))) >> 8;
    t = (v * (255 - ((s * (255 - remainder)) >> 8))) >> 8;

    switch (region) {
        case 6:
        case 0:
            rgb.r = v;
            rgb.g = t;
            rgb.b = p;
            break;
        case 1:
            rgb.r = q;
            rgb.g = v;
            rgb.b = p;
            break;
        case 2:
            rgb.r = p;
            rgb.g = v;
            rgb.b = t;
            break;
        case 3:
            rgb.r = p;
            rgb.g = q;
            rgb.b = v;
            break;
        case 4:
            rgb.r = t;
            rgb.g = p;
            rgb.b = v;
            break;
        default:
            rgb.r = v;
            rgb.g = p;
            rgb.b = q;
            break;
    }

    return rgb;
}
