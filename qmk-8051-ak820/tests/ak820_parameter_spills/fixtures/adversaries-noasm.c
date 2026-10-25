#include <stdint.h>
uint16_t normal(uint16_t value) { return (uint16_t)(value + 1); }
uint16_t volatile_parameter(volatile uint16_t value) { return (uint16_t)(value + 1); }
uint16_t volatile_pointee(const volatile __xdata uint8_t *p) { return (uint16_t)p[0] | ((uint16_t)p[1] << 8); }
uint16_t plain_pointer(const __xdata uint8_t *p) { return (uint16_t)p[0] | ((uint16_t)p[1] << 8); }
uint16_t volatile_pointer(const __xdata uint8_t * volatile p) { return (uint16_t)p[0] | ((uint16_t)p[1] << 8); }
static uint16_t __xdata * __xdata escape;
void leak(uint16_t __xdata *p) { escape = p; }
uint16_t escaped_parameter(uint16_t value) { leak(&value); return value; }
typedef volatile uint16_t hidden_volatile_type;
uint16_t macro_hidden_volatile(hidden_volatile_type value) { return (uint16_t)(value + 1); }
