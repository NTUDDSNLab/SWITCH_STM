#ifndef _PARAM_H_
#define _PARAM_H_

#ifdef CONTENTION_INTENSITY
# define ci_alpha                           0.5 /* TODO: hyper-parameter of alpha */
# define CI_THRESHOLD                       0.5 /* FIXME: Find a proper */
#endif /* CONTENTION_INTENSITY */

#ifdef SWITCH_STM
# define MAX_COR_PER_THREAD                 5     /* Maximum coroutine per thread */
#endif /* SWITCH_STM */

/* Scheduling Policy 0: randomo select, 1: sequence 2: less abort first*/
#define SCHEDULE_POLICY                     0 

#endif /* _PARAM_H_ */
