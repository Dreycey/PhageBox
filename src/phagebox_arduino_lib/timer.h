/*
 * Descripton:
 *     This module contains the timer(s) used
 *     by the phagebox software. These timers 
 *     are used to ensure accurate timing for the 
 *     finite state machine imlimentation of PCR.
 * 
 *     The timer works by cauing an interupt after 
 *     one second and incrementing a counter.
 */
#ifndef  timer_h                                                            
#define timer_h                                                    

// Check Arduino                                                                      
#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
 #include <pins_arduino.h>
#endif

/*
 * Function: 
 *     init_timer()
 * Description:
 *     This method initializes a timer using a bare-metal 
 *     approach to ativate different registers giving a 1-second
 *     controllable interupt-based timer.
 * Input:
 *     void/NA
 * Output: 
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void init_timer();

/*
 * Function: 
 *     adv_delay()
 * Description:
 *     This method stands for "Advanced Delay". It uses a timer 
 *     to cause a delaay specified in seconds
 * Input:
 *     1. seconds to delay for
 * Output: 
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void adv_delay(int seconds2delay);

/*
 * Function: 
 *     reset_timer()
 * Description:
 *     This method rests a timer. The input is a pointer to an int.
 * Input:
 *     1. pointer to int.
 * Output: 
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void reset_timer(volatile int* timer);

/*
 * Function: 
 *     get_timer_1()
 * Description:
 *     Returns pointer to volatile pointer used for timing.
 * Input:
 *     1. pointer to int.
 * Output: 
 *     void/NA
 * Error Handling:
 *     void/NA
 */
volatile int*  get_timer_1();

/*
 * Function: 
 *     get_timer_2()
 * Description:
 *     Returns pointer to volatile pointer used for timing.
 * Input:
 *     1. pointer to int.
 * Output: 
 *     void/NA
 * Error Handling:
 *     void/NA
 */
volatile int*  get_timer_2();

#endif