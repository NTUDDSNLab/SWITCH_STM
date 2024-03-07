#include "switch_table.h"
#ifdef SWITCH_STM
/* ################################################################### *
 * SWITCH_TABLE INITIALIZATION
 * ################################################################### * */
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
    ca->sstk = aco_share_stack_new(0);
    
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
    aco_share_stack_destroy(ca->sstk);
    ca->sstk = NULL;

    free(ca);
}

coroutine_t*
coroutine_array_newCo(coroutine_array_t* ca, void (*coro_func)(void), void* coro_arg)
{
    /* Find the next available slot in the array */
    int index = -1;
    for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
        if (ca->array[i].co == NULL) {
            index = i;
            break;
        }
    }

    /* If there is no room for new coroutine */
    if (index == -1) {
        return NULL;
    }

    /* Create the coroutine */
    coroutine_t* cor = &(ca->array[index]);
    cor->co = aco_create(ca->main_co, ca->sstk, 0, coro_func, coro_arg);
    cor->tx = NULL;
    cor->abort_count = 0;
    cor->coro_func = coro_func;
    cor->coro_arg = coro_arg;

    return cor;
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
};
/*
switch_entry_t*
switch_entry_create(int entry_id)
{
    switch_entry_t* se = (switch_entry_t*)malloc(sizeof(switch_entry_t));
    se->size = 0;
    se->id = entry_id;
    se->list = (coroutine_t**)malloc(sizeof(coroutine_t*) * MAX_COR_PER_THREAD);
    return se;
}
*/

/*
void
switch_entry_delete(switch_entry_t* se)
{
    free(se->list);
    free(se);
}
*/
/*
switch_table_t*
switch_table_create(int max_tx_nb)
{
    switch_table_t* st = (switch_table_t*)malloc(sizeof(switch_table_t));
    st->max_tx_nb = max_tx_nb;
    st->rows = (switch_entry_t**)malloc(sizeof(switch_entry_t*) * max_tx_nb);
    st->size = 1; // The main_co is stored in index 0

    // Create coroutine array 
    st->array = (coroutine_t*)malloc(sizeof(coroutine_t) * MAX_COR_PER_THREAD);
    for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
        st->array[i].co = NULL;
        st->array[i].tx = NULL;
        st->array[i].status = -1;
        st->array[i].coro_arg = NULL;
        st->array[i].coro_func = NULL;
    }
    st->main_co = aco_create(NULL, NULL, 0, NULL, NULL);
    st->sstk = aco_share_stack_new(0);
    st->array[0].co = st->main_co;
    st->cur_co = &(st->array[0]);
    st->isMain = true;

    // Create switching table 
    for (int i = 0; i < max_tx_nb; i++) {
        st->rows[i] = switch_entry_create(i);
    }
    return st;
}
*/
/*
void
switch_table_delete(switch_table_t* st)
{
#ifdef DEBUG_COR
    assert(st != NULL);
    assert(st->array != NULL);
    assert(st->size == 0);

    // Check if all coroutines in the st are finished 
    for (int i=0; i < MAX_COR_PER_THREAD; i++) {
        assert(st->array[i].status == -1);
        assert(st->array[i].co == NULL);
        assert(st->array[i].tx == NULL);
    }
#endif // DEBUG_COR 
    
    // Destory the coroutine array 
    for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
        if (st->array[i].co != NULL) {
            aco_destroy(st->array[i].co);
            st->array[i].co = NULL;
            st->array[i].tx = NULL;
            st->array[i].coro_arg = NULL;
            st->array[i].coro_func = NULL;
        }
    }
    free(st->array);
    st->array = NULL;

    // Destroy the sstk 
    aco_share_stack_destroy(st->sstk);
    st->sstk = NULL;
    st->main_co = NULL;

    // Destroy the switch table 
    for (int i = 0; i < st->max_tx_nb; i++) {
        switch_entry_delete(st->rows[i]);
    }
    free(st->rows);
    free(st);
}
*/
/*
coroutine_t*
switch_table_newCo(switch_table_t* st, void (*coro_func)(void), void* coro_arg, int tx_id)
{
#ifdef DEBUG_COR
    assert(st != NULL);
    assert(st->array != NULL);
    assert(st->size < st->capacity);
#endif // DEBUG_COR 

    // Check if the entry of tx_id is full
    switch_entry_t* se = st->rows[tx_id];
    if (se->size == MAX_COR_PER_THREAD) {
        return NULL;
    }

    // Find the next available slot in the array 
    int index = -1;
    for (int i = 0; i < MAX_COR_PER_THREAD; i++) {
        if (st->array[i].co == NULL) {
            index = i;
            break;
        }
    }

    // If there is no room for new coroutine 
    if (index == -1) {
        return NULL;
    }

    // Create the coroutine 
    coroutine_t* cor = &(st->array[index]);
    cor->co = aco_create(st->main_co, st->sstk, 0, coro_func, coro_arg);
    cor->tx = NULL;
    cor->status = -1;
    cor->coro_func = coro_func;
    cor->coro_arg = coro_arg;
    st->size++;

    // Add the address to the end of entry[tx_id] 
    se->list[se->size] = cor;
    (se->size)++;


    return cor;
}
*/

/* ################################################################### *
 * SCHEDULING FUNCTIONS
 * ################################################################### * */

/*
coroutine_t*
switch_table_get(switch_table_t* st, int tx_id)
{
#ifdef DEBUG_COR
    if (tx_id > st->max_tx_nb) {
        printf("tx_id: %d, max_tx_nb: %d\n", tx_id, st->max_tx_nb);
        assert(0);
    }
#endif // DEBUG_COR 

    if (st->rows[tx_id]->size == 0) {
        return NULL;
    } else {
        coroutine_t* cor = NULL;
        switch_entry_t* se = st->rows[tx_id];
        cor = se->list[se->size - 1];
        return cor;
    }
}
*/
/*
bool
switch_table_add(switch_table_t* st, int tx_id, coroutine_t* cor)
{
#ifdef DEBUG_COR
    if (tx_id > st->max_tx_nb) {
        printf("tx_id: %d, max_tx_nb: %d\n", tx_id, st->max_tx_nb);
        assert(0);
    }
#endif // DEBUG_COR 

    switch_entry_t* se = st->rows[tx_id];
    if (se->size == MAX_COR_PER_THREAD) {
        return -1;
    } else {
        se->list[se->size] = cor;
        se->size++;
        return 0;
    }
}
*/
/*
bool 
switch_table_isEmpty(switch_table_t* st, int tx_id)
{
#ifdef DEBUG_COR
    if (tx_id > st->max_tx_nb) {
        printf("tx_id: %d, max_tx_nb: %d\n", tx_id, st->max_tx_nb);
        assert(0);
    }
#endif // DEBUG_COR 

    switch_entry_t* se = st->rows[tx_id];
    if (se->size == 0) {
        return true;
    } else {
        return false;
    }
}
*/
/*
bool
switch_table_swap(switch_table_t* st, int tx_id_src, int tx_id_dst)
{
#ifdef DEBUG_COR
    if (tx_id_src > st->max_tx_nb || tx_id_dst > st->max_tx_nb) {
        printf("tx_id_src: %d, tx_id_dst: %d, max_tx_nb: %d\n", tx_id_src, tx_id_dst, st->max_tx_nb);
        assert(0);
    }
#endif // DEBUG_COR 

    if (tx_id_src == tx_id_dst) {
        return -1;
    }
    switch_entry_t* se_src = st->rows[tx_id_src];
    switch_entry_t* se_dst = st->rows[tx_id_dst];
    if (se_src->size == 0 || se_dst->size == MAX_COR_PER_THREAD) {
        return -1;
    }
    coroutine_t* cor_src = se_src->list[se_src->size - 1];
    se_src->size--;
    se_dst->list[se_dst->size] = cor_src;
    se_dst->size++;
    return 0;
}
*/

#endif /* SWITCH_STM */
