#ifndef _SWITCHER_H_
#define _SWITCHER_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "switch_table.h"
#include "param.h"
#include "aco.h"
#include "thread.h"

extern __thread struct coroutine * cur_cor;
extern __thread struct coroutine_array * cor_array;
extern long switch_numThread;
#ifdef SWITCH_STM_TIME_PROFILE
extern __thread unsigned long run_tx_time_sum;
extern __thread unsigned long switch_time_sum;
extern __thread unsigned long stage1_time_sum;
extern __thread unsigned long stage2_time_sum;
extern __thread unsigned long do_switch_count;
extern __thread unsigned long no_switch_count;
__thread struct timespec run_tx_start_time, run_tx_end_time;
__thread struct timespec switch_start_time, switch_end_time;
__thread struct timespec stage_start_time, stage_end_time;
#endif /* SWITCH_STM_TIME_PROFILE */
bool thread_barrier_exist = false;
unsigned int switching_count = 0;

#ifdef CONTENTION_INTENSITY
extern __thread float contention_intensity;
#endif /* CONTENTION_INTENSITY */

void
switcher_init(coroutine_array_t** ca, void (*funcPtr)(void))
{
      srand(clock());
      aco_thread_init(NULL);
      *ca = coroutine_array_create();

      if (coroutine_array_newCo(*ca, funcPtr, NULL) == false){
         printf("Error creating coroitine!!!\n");
         exit(1);
      };
}

unsigned int
switcher_decide(coroutine_array_t* ca, int cur_decision)
{  
   static int decision = 0;
   int min_abort_count;
   switch (SCHEDULE_POLICY) {
      case 0:
         //random
         while(cur_decision == decision){
            decision = rand() % MAX_COR_PER_THREAD;
         }
         break;

      case 1:
         //sequence
         decision = decision + 1;
         decision = decision % MAX_COR_PER_THREAD;
         break;

      case 2:
         // less abort first
         decision = 0;
         coroutine_t * cor = coroutine_array_get(cor_array,0); 
         min_abort_count = cor->abort_count;
         
         for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
            cor = coroutine_array_get(cor_array,i); 
            if (cor->co->is_end == 0) {
               decision = i;
               min_abort_count = cor->abort_count;
               break;
             }
         }
         for (int i = decision; i < MAX_COR_PER_THREAD; i++) {
            cor = coroutine_array_get(cor_array,i);
            if (cor->abort_count < min_abort_count && cor->co->is_end == 0 && cor->unswitchable == 0) {
               decision = i;
               min_abort_count =cor->abort_count;
            }
         }

         break;
   }
   return decision;
}

void
switcher_run(coroutine_array_t** ca)
{
   #ifdef SWITCH_STM_TIME_PROFILE 
   clock_gettime(CLOCK_MONOTONIC, &switch_start_time);
   long run_tx_time_round = 0;
   #endif /* SWITCH_STM_TIME_PROFILE */
   //Initialize a counter to count how many cor is done
   int finished_cor_counter = 0;
   volatile unsigned int rnd_wait;
   //Pick a coroutine 
   cur_cor = coroutine_array_get(*ca, 0);

   #ifdef SWITCH_STM_TIME_PROFILE 
   clock_gettime(CLOCK_MONOTONIC, &stage_start_time);
   #endif /* SWITCH_STM_TIME_PROFILE */

   //then run that coroutine, if abort then switch to another
   while(1){
      #ifdef SWITCH_STM_TIME_PROFILE 
      clock_gettime(CLOCK_MONOTONIC, &run_tx_start_time);
      #endif /* SWITCH_STM_TIME_PROFILE */
      aco_resume(cur_cor->co);
     #ifdef SWITCH_STM_TIME_PROFILE  
      clock_gettime(CLOCK_MONOTONIC, &run_tx_end_time);
      run_tx_time_round = run_tx_time_round + (run_tx_end_time.tv_sec - run_tx_start_time.tv_sec) * 1000000000 + (run_tx_end_time.tv_nsec - run_tx_start_time.tv_nsec); 
      #endif /* SWITCH_STM_TIME_PROFILE */
      if(cur_cor->co->is_end == 1){
         finished_cor_counter++;
         break;
      }
      else{
         rnd_wait = rand() % switch_numThread;
         for(int i = 0; i < rnd_wait;i++){
            // do noting but wait
         }
         /* if rnd <= wait_count means high serialization affinity */
         if (thread_barrier_exist == false){
         #ifdef CONTENTION_INTENSITY
            if (contention_intensity >= CI_THRESHOLD){ 
         #endif /* !CONTENTION_INTENSITY */
                  /* do switch */
                  cur_cor = coroutine_array_get(*ca, switcher_decide(*ca,coroutine_index_get(cur_cor)));
                  #ifdef SWITCH_STM_TIME_PROFILE
                  do_switch_count++;
                  #endif /* SWITCH_STM_TIME_PROFILE */
         #ifdef CONTENTION_INTENSITY
            }
            else{//contention_intensity <= CI_THRESHOLD
               #ifdef SWITCH_STM_TIME_PROFILE
               no_switch_count++;
               #endif /* SWITCH_STM_TIME_PROFILE */
            }
         #endif /* !CONTENTION_INTENSITY */
         }    
         else{
            #ifdef SWITCH_STM_TIME_PROFILE
            no_switch_count++;
            #endif /* SWITCH_STM_TIME_PROFILE */   
         }
      }
   }
   #ifdef SWITCH_STM_TIME_PROFILE
   clock_gettime(CLOCK_MONOTONIC, &stage_end_time);
   stage1_time_sum = stage1_time_sum + (stage_end_time.tv_sec - stage_start_time.tv_sec) * 1000000000 + (stage_end_time.tv_nsec - stage_start_time.tv_nsec);

   clock_gettime(CLOCK_MONOTONIC, &stage_start_time);
   #endif /* SWITCH_STM_TIME_PROFILE */ 
   //if thread barrier exist, don't finish the rest coroutines
   if(thread_barrier_exist == true){
         goto delete_ca;
      } 

   //finish the rest coroutine
   while(finished_cor_counter < MAX_COR_PER_THREAD)
   {
      //choose a cor which is not finished
      while(cur_cor->co->is_end == 1)
      {
         cur_cor = coroutine_array_get(*ca, switcher_decide(*ca,coroutine_index_get(cur_cor)));
      }
      #ifdef SWITCH_STM_TIME_PROFILE
      clock_gettime(CLOCK_MONOTONIC, &run_tx_start_time);
      #endif /* SWITCH_STM_TIME_PROFILE */ 
      aco_resume(cur_cor->co);
      #ifdef SWITCH_STM_TIME_PROFILE
      clock_gettime(CLOCK_MONOTONIC, &run_tx_end_time);
      run_tx_time_round = run_tx_time_round + (run_tx_end_time.tv_sec - run_tx_start_time.tv_sec) * 1000000000 + (run_tx_end_time.tv_nsec - run_tx_start_time.tv_nsec); 
      #endif /* SWITCH_STM_TIME_PROFILE */ 
      //if cor is finished, add the counter
      if(cur_cor->co->is_end == 1){
         finished_cor_counter++;
      } 
   }
   #ifdef SWITCH_STM_TIME_PROFILE
   clock_gettime(CLOCK_MONOTONIC, &stage_end_time);
   stage2_time_sum = stage2_time_sum + (stage_end_time.tv_sec - stage_start_time.tv_sec) * 1000000000 + (stage_end_time.tv_nsec - stage_start_time.tv_nsec);
   #endif /* SWITCH_STM_TIME_PROFILE */  
   //delete the switch_table
   delete_ca:
   coroutine_array_delete(*ca);
   
   //caculate the time spent on switch
   #ifdef SWITCH_STM_TIME_PROFILE
   clock_gettime(CLOCK_MONOTONIC, &switch_end_time);
   switch_time_sum = switch_time_sum 
                     +(switch_end_time.tv_sec - switch_start_time.tv_sec) * 1000000000 + (switch_end_time.tv_nsec - switch_start_time.tv_nsec)
                     -run_tx_time_round;
   run_tx_time_sum = run_tx_time_sum + run_tx_time_round;
   #endif /* SWITCH_STM_TIME_PROFILE */ 
}

#endif // _SWITCHER_H_