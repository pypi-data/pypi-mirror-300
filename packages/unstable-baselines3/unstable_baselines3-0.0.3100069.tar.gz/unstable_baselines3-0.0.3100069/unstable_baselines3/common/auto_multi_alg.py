from pettingzoo import AECEnv, ParallelEnv

from typing import Union

from unstable_baselines3.common.parallel_alg import ParallelAlgorithm
from unstable_baselines3.common.aec_alg import AECAlgorithm


def AutoMultiAgentAlgorithm(
        env: Union[AECEnv, ParallelEnv],
        workers,
        worker_infos=None,
        *args,
        **kwargs, ) -> Union[AECAlgorithm, ParallelAlgorithm]:
    env.reset()
    if isinstance(env, AECEnv):
        return AECAlgorithm(env=env,
                            workers=workers,
                            worker_infos=worker_infos,
                            *args,
                            **kwargs,
                            )
    elif isinstance(env, ParallelEnv):
        return ParallelAlgorithm(parallel_env=env,
                                 workers=workers,
                                 worker_infos=worker_infos,
                                 *args,
                                 **kwargs,
                                 )
    else:
        raise Exception('env not recognized:', env)
