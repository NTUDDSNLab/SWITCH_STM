#ifndef _SWITCH_TABLE_H_
#define _SWITCH_TABLE_H_

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "aco.h"
#include "param.h"

#ifdef DEBUG_COR
#include <assert.h>
#endif /* DEBUG_COR */

#ifdef SWITCH_STM
struct stm_tx;

typedef struct coroutine {
    aco_t* co;
    struct stm_tx* tx;
    int index;
#ifdef EPOCH_GC
    long gc;
#endif /* EPOCH_GC */
    int status;
    int abort_count;
    void (*coro_func)(void);
    void *coro_arg;
} coroutine_t;

typedef struct coroutine_array{
    coroutine_t* array;
    aco_share_stack_t** sstk;
    aco_t* main_co;
} coroutine_array_t;


/* ################################################################### *
 * Initialization
 * ################################################################### * */

coroutine_array_t* coroutine_array_create(void);

void coroutine_array_delete(coroutine_array_t* ca);

bool coroutine_array_newCo(coroutine_array_t* ca, void (*coro_func)(void), void* coro_arg);

coroutine_t* coroutine_array_get(coroutine_array_t* ca, int cor_index);

int coroutine_index_get(coroutine_t* c);

#endif /* SWITCH_STM */
#ifdef __cplusplus
} 
#endif // __cplusplus

#endif // _SWITCH_TABLE_H_