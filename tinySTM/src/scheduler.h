#ifndef _SCHEDULER_H_
#define _SCHEDULER_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "switch_table.h"
#include "param.h"
#include "aco.h"
#include "thread.h"

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
scheduler_decide()
{  
   static unsigned int rnd = 0; 
   //rnd = 1;

   rnd = rand() % MAX_COR_PER_THREAD;

   /*
   rnd++;
   rnd = rnd % MAX_COR_PER_THREAD;
   if(rnd == 0){
      rnd ++;
   }
   */

   //printf("\nrnd : %d",rnd);
   //fflush(stdout);
   return rnd;
}

extern __thread struct coroutine * cur_cor;

void
scheduler_run(coroutine_array_t** ca)
{
   //First pick a coroutine 
   cur_cor = coroutine_array_get(*ca, scheduler_decide());

   //then run that coroutine, if rollback then switch to another
   while(1){
      aco_resume(cur_cor->co);
      if(cur_cor->co->is_end == 1){
         break;
      }
      else{
         cur_cor = coroutine_array_get(*ca, scheduler_decide());
      }
   }

   //finish the rest coroutine
   for(int i = 0; i < MAX_COR_PER_THREAD; i++){
      cur_cor = coroutine_array_get(*ca, i);
      while(cur_cor->co->is_end == 0){
         aco_resume(cur_cor->co);
      }
      assert(cur_cor->co->is_end);
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