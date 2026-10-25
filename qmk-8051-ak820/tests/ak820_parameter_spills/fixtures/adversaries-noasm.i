#line 0 "/research/adversaries-noasm.c"
#line 0 "<built-in>"
#line 0 "<command-line>"
#line 1 "/research/adversaries-noasm.c"
#line 1 "/toolchains/sdcc-4.6.0/share/sdcc/include/stdint.h" 3 4
#line 46 "/toolchains/sdcc-4.6.0/share/sdcc/include/stdint.h" 3 4
typedef signed char int8_t;
typedef short int int16_t;
typedef long int int32_t;

typedef long long int int64_t;



typedef unsigned char uint8_t;
typedef unsigned short int uint16_t;
typedef unsigned long int uint32_t;

typedef unsigned long long int uint64_t;





typedef signed char int_least8_t;
typedef short int int_least16_t;
typedef long int int_least32_t;

typedef long long int int_least64_t;



typedef unsigned char uint_least8_t;
typedef unsigned short int uint_least16_t;
typedef unsigned long int uint_least32_t;

typedef unsigned long long int uint_least64_t;





typedef signed char int_fast8_t;
typedef int int_fast16_t;
typedef long int int_fast32_t;

typedef long long int int_fast64_t;



typedef unsigned char uint_fast8_t;
typedef unsigned int uint_fast16_t;
typedef unsigned long int uint_fast32_t;

typedef unsigned long long int uint_fast64_t;






  typedef long int intptr_t;
  typedef unsigned long int uintptr_t;
#line 114 "/toolchains/sdcc-4.6.0/share/sdcc/include/stdint.h" 3 4
typedef long long int intmax_t;
typedef unsigned long long int uintmax_t;
#line 2 "/research/adversaries-noasm.c"
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
