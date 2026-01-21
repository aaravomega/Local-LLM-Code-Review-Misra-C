#include <stdio.h>
#include <stdlib.h>

// MACROS
#define max_value 100  // MISRA Violation: Macro constants should usually be wrapped or typed
#define calc(x) x * x  // MISRA Violation: Missing parentheses around parameter 'x'

// GLOBAL VARIABLES
int system_status = 0; // Style Violation: Should likely be g_SystemStatus (Company Style)
                       // MISRA Violation: using basic 'int' instead of 'int32_t'

// FUNCTION PROTOTYPES
void process_sensor_data(int input);

int main() {
    int sensorVal = 50;

    // LOGICAL ERROR: Using uninitialized variable (sometimes caught by cppcheck)
    int uninit_var;
    if (sensorVal > max_value) {
        printf("Error: %d", uninit_var);
    }

    process_sensor_data(sensorVal);

    return 0;
}

// Style Violation: Function name is snake_case, you wanted CamelCase
void process_sensor_data(int input) {
    // MEMORY LEAK: Buffer allocated but never freed
    char *buffer = (char*)malloc(256);

    // MISRA Violation: Pointer arithmetic on void pointer (if it were void*)
    // or unsafe buffer handling without size checks.
    sprintf(buffer, "Processing value: %d", input);

    printf("%s\n", buffer);

    // MISRA Violation: Implicit conversion from float to int
    int result = input + 5.5;

    if (result > 10)
        system_status = 1; // MISRA Violation: Missing braces {} for if statement
}