#ifndef _SCHEDULER_H_
#define _SCHEDULER_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "switch_table.h"
#include "param.h"
#include "aco.h"
#include "thread.h"
#include "tm.h"

extern __thread struct coroutine * cur_cor;
extern __thread long switch_time;
extern __thread long switch_time_sum;
struct timespec start_time, end_time;
bool thread_barrier_exist = false;

#ifdef CONTENTION_INTENSITY
extern __thread float contention_intensity;
#endif /* CONTENTION_INTENSITY */

void
scheduler_init(coroutine_array_t** ca, void (*funcPtr)(void))
{
      srand(clock());
      aco_thread_init(NULL);
      *ca = coroutine_array_create();
      
      for (int i =0; i < MAX_COR_PER_THREAD; i++){
         coroutine_array_newCo(*ca, funcPtr, NULL);
      }
}

unsigned int
scheduler_decide(coroutine_array_t* ca)
{  
   static int decision = 0;
   int max_tx_number;
   switch (SCHEDULE_POLICY) {
      case 0:
         //random
         decision = rand() % MAX_COR_PER_THREAD;
         break;

      case 1:
         //sequence
         decision = decision + 1;
         decision = decision % MAX_COR_PER_THREAD;
         break;

      case 2:
         // don't switch
         break;

      case 3:
         //Finish the quick-ending task first
         //FIXME: doesn't switch since the initial coroutine must come with max status 
         max_tx_number = ca->array[0].status;
         decision = 0;
         for (int i =1 ; i < MAX_COR_PER_THREAD; i++){
            if (ca->array[i].status > max_tx_number){
               decision = i;
               max_tx_number = ca->array[i].status; 
            }
         }
         break;

      default:
         //random
         decision = rand() % MAX_COR_PER_THREAD;

   }
   return decision;
}

void
scheduler_run(coroutine_array_t** ca)
{  
   //initialize time recording module
   switch_time = 0;
   clock_gettime(CLOCK_MONOTONIC, &start_time);

   //Initialize a counter to count how many cor is done
   int finished_cor_counter = 0;

   //Pick a coroutine 
   cur_cor = coroutine_array_get(*ca, 0);

   //then run that coroutine, if abort then switch to another
   while(1){
      clock_gettime(CLOCK_MONOTONIC, &end_time);
      switch_time = switch_time + (end_time.tv_sec - start_time.tv_sec) * 1000000000L + (end_time.tv_nsec - start_time.tv_nsec);
      aco_resume(cur_cor->co);
      clock_gettime(CLOCK_MONOTONIC, &start_time);
      if(cur_cor->co->is_end == 1){
         finished_cor_counter++;
         break;
      }
      else{
         #ifdef CONTENTION_INTENSITY
         if (thread_barrier_exist == false && contention_intensity > CI_THRESHOLD){
         #else  /* !CONTENTION_INTENSITY */
         if (thread_barrier_exist == false){
         #endif /* !CONTENTION_INTENSITY */
            cur_cor = coroutine_array_get(*ca, scheduler_decide(*ca));
         }
      }
   }
   
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
         cur_cor = coroutine_array_get(*ca, scheduler_decide(*ca));
      }
      clock_gettime(CLOCK_MONOTONIC, &end_time);
      switch_time = switch_time + (end_time.tv_sec - start_time.tv_sec) * 1000000000L + (end_time.tv_nsec - start_time.tv_nsec);
      aco_resume(cur_cor->co);
      clock_gettime(CLOCK_MONOTONIC, &start_time);
      //if cor is finished, add the counter
      if(cur_cor->co->is_end == 1){
         finished_cor_counter++;
      } 
   }
   
   //delete the switch_table
   delete_ca:
   coroutine_array_delete(*ca);
   
   //caculate the time spent on switch
   clock_gettime(CLOCK_MONOTONIC, &end_time);
   switch_time = switch_time + (end_time.tv_sec - start_time.tv_sec) * 1000000000L + (end_time.tv_nsec - start_time.tv_nsec);
   switch_time_sum = switch_time_sum + switch_time;
}

/* Decide which task to execute next.
 * If contention is detected -> proactive instantiation or switch to pending task
 * else keep normal execution
 * 
 * Update CTT info to instruct next iteration.
 * 
 * condition types: 
    0: main co enters TM_THREAD_EXIT()
    1: non-main co enters TM_THREAD_EXIT()
    2: main co enters stm_rollback()
    3: non-main co enters stm_rollback()
 */
/*
static inline void
coro_thread_exit(switch_table_t* st)
{
   // Check if the current coroutine is main_co 
   if (st->isMain()) {
      // Check if there are pending task in switching table 
      if (st->size == 0) return;
      else {
         
      }
   }


}


static inline void
coro_stm_rollback()
{

}
*/


// TODO: Unfinished
// static inline void
// switchstm_scheduler(int condition, coroutine_table_t *ct, switch_table_t *st)
// {
//     switch (condition) {
//         // main co enters TM_THREAD_EXIT()
//         case 0:
//             coroutine_t *src_co = ct->cur_co;

//             // Check if there are pending tasks
//             for (int i = 0; i < st->max_tx_nb; i++) {
//                 if (switch_table_isEmpty(st, i) == 0) continue;
//                 else {
//                     // If there are pending tasks, switch to the first one
//                     coroutine_t *des_co = switch_table_get(st, i);

//                 }
//             }

//             // If there are no pending tasks, switch to the main co
//             break;
            

//     }
// }



#endif // _SCHEDULER_H_