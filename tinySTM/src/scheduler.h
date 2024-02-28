#ifndef _SCHEDULER_H_
#define _SCHEDULER_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "switch_table.h"
#include "param.h"
#include "aco.h"
#include "thread.h"

extern __thread struct coroutine * cur_cor;
extern long switch_numThread;
extern __thread unsigned long run_tx_time_sum;
extern __thread unsigned long switch_time_sum;
extern __thread unsigned long stage1_time_sum;
extern __thread unsigned long stage2_time_sum;
extern __thread unsigned long do_switch_count;
extern __thread unsigned long no_switch_count;
__thread struct timespec run_tx_start_time, run_tx_end_time;
__thread struct timespec switch_start_time, switch_end_time;
__thread struct timespec stage_start_time, stage_end_time;
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
scheduler_decide(coroutine_array_t* ca, int cur_decision)
{  
   static int decision = 0;
   int max_tx_number;
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
         // don't switch
         break;

      default:
         //random
         while(cur_decision == decision){
            decision = rand() % MAX_COR_PER_THREAD;
         }
         break;

   }
   return decision;
}

void
scheduler_run(coroutine_array_t** ca)
{ 
   clock_gettime(CLOCK_MONOTONIC, &switch_start_time);
   long run_tx_time_round = 0;
   //Initialize a counter to count how many cor is done
   int finished_cor_counter = 0;

   //Pick a coroutine 
   cur_cor = coroutine_array_get(*ca, 0);

   clock_gettime(CLOCK_MONOTONIC, &stage_start_time);
   //then run that coroutine, if abort then switch to another
   while(1){
      clock_gettime(CLOCK_MONOTONIC, &run_tx_start_time);
      aco_resume(cur_cor->co);
      clock_gettime(CLOCK_MONOTONIC, &run_tx_end_time);
      run_tx_time_round = run_tx_time_round + (run_tx_end_time.tv_sec - run_tx_start_time.tv_sec) * 1000000000 + (run_tx_end_time.tv_nsec - run_tx_start_time.tv_nsec); 
      if(cur_cor->co->is_end == 1){
         finished_cor_counter++;
         break;
      }
      else{
         if (thread_barrier_exist == false){
#        ifdef CONTENTION_INTENSITY
            if (contention_intensity <= CI_THRESHOLD){ 
#        endif /* !CONTENTION_INTENSITY */
               cur_cor = coroutine_array_get(*ca, scheduler_decide(*ca,coroutine_index_get(cur_cor)));
               do_switch_count++;
#        ifdef CONTENTION_INTENSITY
            }
            
            else{//contention_intensity >= CI_THRESHOLD
                
               int random_wait = rand() % (switch_numThread<<3);
               for(long i = 0;i < random_wait;i++){
                  //do nothing
               }
               
               int switch_rnd = rand() % 100;
               for(int i = 0;i < switch_rnd;i++){
                  //do nothing
               }
               no_switch_count++;
            }
            
#     endif /* !CONTENTION_INTENSITY */
         }    
         else{
            no_switch_count++;   
         }
      }
   }
   clock_gettime(CLOCK_MONOTONIC, &stage_end_time);
   stage1_time_sum = stage1_time_sum + (stage_end_time.tv_sec - stage_start_time.tv_sec) * 1000000000 + (stage_end_time.tv_nsec - stage_start_time.tv_nsec);

   clock_gettime(CLOCK_MONOTONIC, &stage_start_time);
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
         cur_cor = coroutine_array_get(*ca, scheduler_decide(*ca,coroutine_index_get(cur_cor)));
      }
      clock_gettime(CLOCK_MONOTONIC, &run_tx_start_time);
      aco_resume(cur_cor->co);
      clock_gettime(CLOCK_MONOTONIC, &run_tx_end_time);
      run_tx_time_round = run_tx_time_round + (run_tx_end_time.tv_sec - run_tx_start_time.tv_sec) * 1000000000 + (run_tx_end_time.tv_nsec - run_tx_start_time.tv_nsec); 
      //if cor is finished, add the counter
      if(cur_cor->co->is_end == 1){
         finished_cor_counter++;
      } 
   }
   clock_gettime(CLOCK_MONOTONIC, &stage_end_time);
   stage2_time_sum = stage2_time_sum + (stage_end_time.tv_sec - stage_start_time.tv_sec) * 1000000000 + (stage_end_time.tv_nsec - stage_start_time.tv_nsec);
   
   //delete the switch_table
   delete_ca:
   coroutine_array_delete(*ca);
   
   //caculate the time spent on switch
   clock_gettime(CLOCK_MONOTONIC, &switch_end_time);
   switch_time_sum = switch_time_sum 
                     +(switch_end_time.tv_sec - switch_start_time.tv_sec) * 1000000000 + (switch_end_time.tv_nsec - switch_start_time.tv_nsec)
                     -run_tx_time_round;
   run_tx_time_sum = run_tx_time_sum + run_tx_time_round;
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