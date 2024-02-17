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
/*
typedef struct coroutine {
    aco_t* co;
    struct stm_tx* tx;
    int status;                     // -1: Unused or finished, others: current executing tx_number 
    void (*coro_func)(void);
    void *coro_arg;
} coroutine_t;
*/

typedef struct coroutine {
    aco_t* co;
    struct stm_tx* tx;
    int index;
#ifdef EPOCH_GC
    long gc;
#endif /* EPOCH_GC */
    int status;
    void (*coro_func)(void);
    void *coro_arg;
} coroutine_t;

typedef struct coroutine_array{
    coroutine_t* array;
    aco_share_stack_t* sstk;
    aco_t* main_co;
} coroutine_array_t;

/*
typedef struct switch_entry {
    coroutine_t** list;             // Array of coroutine_t*, the size is MAX_COROUTINE 
    int size;                       // The number of coroutine valid in the entry 
    int id;                         // The ID of the current executing transaction 
} switch_entry_t;

typedef struct switch_table {
    switch_entry_t** rows;          // Array of switch_entry_t, the size is MAX_TX
    coroutine_t* array;             // Array of coroutine_t
    coroutine_t* cur_co;            // Pointer to the current coroutine
    bool isMain;                    // Figure out if the current coroutine is main
    aco_share_stack_t* sstk;        // Pointer to the shared stack
    aco_t* main_co;                 // Pointer the main_co, which is stored in index 0 of the array
    int max_tx_nb;                  // #rows, The maximum transaction state
    int size;                       // The number of coroutine valid in the table
} switch_table_t;
*/

/* ################################################################### *
 * Initialization
 * ################################################################### * */

coroutine_array_t* coroutine_array_create(void);

void coroutine_array_delete(coroutine_array_t* ca);

coroutine_t* coroutine_array_newCo(coroutine_array_t* ca, void (*coro_func)(void), void* coro_arg);

coroutine_t* coroutine_array_get(coroutine_array_t* ca, int cor_index);

int coroutine_index_get(coroutine_t* c);
/*
switch_entry_t* switch_entry_create(int entry_id);

void switch_entry_delete(switch_entry_t* se);

switch_table_t* switch_table_create(int max_tx_nb); 

void switch_table_delete(switch_table_t* st);
*/

/*
Create new coroutine
    @param:
        st: switching table
        coro_func: the function pointer to the coroutine function
        coro_arg: the void pointer to the coroutine function argument
        tx_id: the transaction id of the new coroutine
    @return:
        NULL: if there is no room for new coroutine
        otherwise: the address of the new corouinte
*/

//coroutine_t* switch_table_newCo(switch_table_t* st, void (*coro_func)(void), void* coro_arg, int tx_id);

/* ################################################################### *
 * Setters and Getters
 * ################################################################### * */

/*
inline coroutine_t* switch_table_getCurCo(switch_table_t* st) { return st->cur_co; }

inline void switch_table_setCurCo(switch_table_t* st, coroutine_t* co) { st->cur_co = co;}

inline struct stm_tx* switch_table_getCurTx(switch_table_t* st) { return st->cur_co->tx; }

inline void switch_table_setCurTx(switch_table_t* st, struct stm_tx* tx) { st->cur_co->tx = tx; }

inline int switch_table_getCurStatus(switch_table_t* st) { return st->cur_co->status; }

inline void switch_table_setCurStatus(switch_table_t* st, int status) { st->cur_co->status = status; }

inline bool switch_table_isMainCo(switch_table_t* st) {return st->isMain; }
*/

/* ################################################################### *
 * Scheduling Functions
 * ################################################################### * */




/* 
Get the pointer of coroutine_t with the given tx_id 
    @param:
        st: the switch_table_t* to be searched
        tx_id: the transaction id
    @return:
        the pointer of coroutine_t, if the tx_id is valid
        NULL, if the tx_id is invalid
*/
//coroutine_t* switch_table_get(switch_table_t* st, int tx_id);

/* 
Set the pointer of coroutine_t with the given tx_id 
    @param:
        st: the switch_table_t* to be added
        tx_id: the transaction id
        co: the pointer of coroutine_t
    @return:
        0, if the tx_id entry is not full
        -1, if the tx_id entry is full
*/
//bool switch_table_add(switch_table_t* st, int tx_id, coroutine_t* co);

//bool switch_table_isEmpty(switch_table_t* st, int tx_id);

/*
Swap the coroutine_t pointer from st->rows[tx_id_src] to st->rows[tx_id_dst]
    @param:
        st: the switch_table_t* to be swapped
        tx_id_src: the transaction id of the source
        tx_id_dst: the transaction id of the destination
    @return:
        0, if the swap is successful
        -1, if the swap is unsuccessful
    @note:
        The swap is unsuccessful if the destination entry is full
        The swap is unsuccessful if the source entry is empty
        The swap is unsuccessful if the source and destination are the same
        The swap is unsuccessful if the source and destination are not valid
*/
//bool switch_table_swap(switch_table_t* st, int tx_id_src, int tx_id_dst);


/*
Determine if the specific tx_id's entry is full
    @param:
        st: the switch_table_t*
        tx_id: the query entry
    @return:
        true: the coresponding entry is full
        false: otherwise
*/

//inline bool switch_table_isFull(switch_table_t* st, int tx_id) { return (st->rows[tx_id]->size == MAX_COR_PER_THREAD);}

#endif /* SWITCH_STM */
#ifdef __cplusplus
} 
#endif // __cplusplus

#endif // _SWITCH_TABLE_H_