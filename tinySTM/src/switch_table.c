#include "switch_table.h"
#ifdef SWITCH_STM
/* ################################################################### *
 * SWITCH_TABLE INITIALIZATION
 * ################################################################### * */
#if defined(SWITCH_STM_TIME_PROFILE) || defined(SWITCH_STM_METRIC_PROFILE)
__thread bool t_just_switched = false;
__thread unsigned long long breakdown_switch_tx_count = 0;
__thread unsigned long long breakdown_commit_after_switch_count = 0;
#endif

coroutine_array_t*
coroutine_array_create(void)
{   
    /* allocate memories */
    coroutine_array_t* ca = (coroutine_array_t*)malloc(sizeof(coroutine_array_t));

    /* allocate memories for each coroutine */
    ca->array = (coroutine_t*)malloc(sizeof(coroutine_t) * MAX_COR_PER_THREAD);
    
    /* initialize each coroutine */
    for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
        ca->array[i].co = NULL;
        ca->array[i].tx = NULL;
        ca->array[i].index = i;
#ifdef EPOCH_GC
        ca->array[i].gc = 0;
#endif /* EPOCH_GC */
        ca->array[i].status = -1;
        ca->array[i].coro_arg = NULL;
        ca->array[i].coro_func = NULL;
    }
    /* initialize main_co */
    ca->main_co = aco_create(NULL, NULL, 0, NULL, NULL);
    
    /* initialize shared stack */
    ca->sstk = malloc(5 * sizeof(aco_share_stack_t*));
    for (int i = 0; i < MAX_COR_PER_THREAD ; i++) {
        ca->sstk[i] = aco_share_stack_new(0);
    }
    
    return ca; 
}

void coroutine_array_delete(coroutine_array_t* ca)
{
   /* Destory the coroutine array */
    for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
        if (ca->array[i].co != NULL) {
            aco_destroy(ca->array[i].co);
            ca->array[i].co = NULL;
            ca->array[i].tx = NULL;
            ca->array[i].coro_arg = NULL;
            ca->array[i].coro_func = NULL;
        }
    }
    free(ca->array);
    ca->array = NULL; 

    /* Destroy main_co */
    aco_destroy(ca->main_co);
    ca->main_co = NULL;

    /* Destroy the sstk */
    for (int i = 0; i < MAX_COR_PER_THREAD ; i++) {
        aco_share_stack_destroy(ca->sstk[i]);
    }
    ca->sstk = NULL;

    free(ca);
}

bool
coroutine_array_newCo(coroutine_array_t* ca, void (*coro_func)(void), void* coro_arg){

    /* Create the coroutine */
    for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
        coroutine_t* cor = &(ca->array[i]);
            if (ca->array[i].status == -1){
            cor->co = aco_create(ca->main_co, ca->sstk[i], 0, coro_func, coro_arg);
            cor->tx = NULL;
            cor->abort_count = 0;
            cor->unswitchable = 0;
            cor->coro_func = coro_func;
            cor->coro_arg = coro_arg;
        }
        else{
            return false;
        }
    }
    return true;
}

coroutine_t*
coroutine_array_get(coroutine_array_t* ca, int cor_index)
{
    coroutine_t* cor = &(ca->array[cor_index]);
    return cor;
}

int coroutine_index_get(coroutine_t* c)
{
    return c->index;
}


#endif /* SWITCH_STM */
