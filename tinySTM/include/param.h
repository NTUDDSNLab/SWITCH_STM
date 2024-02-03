#ifndef _PARAM_H_
#define _PARAM_H_

#ifdef CT_TABLE
# define TOTAL_CONTEXT_NUM                  15 /* TODO: Auto set by the maximum transactions correspoding to application */
#endif /* CT_TABLE */

#ifdef CONTENTION_INTENSITY
# define ci_alpha                           0.449     /* TODO: hyper-parameter of alpha */
# define CI_THRESHOLD                       0.5 /* FIXME: Find a proper */
#endif /* CONTENTION_INTENSITY */

#ifdef SWITCH_STM
# define MAX_COR_PER_THREAD                 5     /* Maximum coroutine per thread */
#endif /* SWITCH_STM */

/* Scheduling Policy 0: randomo select, 1: sequence 2: don't switch 3: Finish the quick-ending task first*/
#define SCHEDULE_POLICY                     3

#endif /* _PARAM_H_ */
