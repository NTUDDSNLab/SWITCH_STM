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
   static unsigned int decision = 0; 
   int max_tx_number;
   switch (SCHEDULE_POLICY) {
      case 0:
         //random
         decision = rand() % MAX_COR_PER_THREAD;
         break;

      case 1:
         //sequence
         decision++;
         decision = decision % MAX_COR_PER_THREAD;
         break;

      case 2:
         // don't switch
         break;

      case 3:
         //Finish the quick-ending task first
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

extern __thread struct coroutine * cur_cor;
bool thread_barrier_exist = false;
void
scheduler_run(coroutine_array_t** ca)
{
   //First pick a coroutine 
   cur_cor = coroutine_array_get(*ca, 0);

   //then run that coroutine, if rollback then switch to another
   while(1){
      aco_resume(cur_cor->co);
      if(cur_cor->co->is_end == 1){
         break;
      }
      else{
         if (thread_barrier_exist == false){
            cur_cor = coroutine_array_get(*ca, scheduler_decide(*ca));
         }
      }
   }

   //finish the rest coroutine
   for(int i = 0; i < MAX_COR_PER_THREAD; i++){
      cur_cor = coroutine_array_get(*ca, i);
      // check weather thread barrier exist 
      if(thread_barrier_exist == false){
         // thread barrier not exist, the remain coroutine should be finish
         while(cur_cor->co->is_end == 0){
            aco_resume(cur_cor->co);
         }
         //assert(cur_cor->co->is_end);
      }
      else{
          // thread barrier exist, directly exit the the thread for coroutine
         //TM_THREAD_EXIT();
      }
   }
   
   //delete the switch_table
   coroutine_array_delete(*ca);
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