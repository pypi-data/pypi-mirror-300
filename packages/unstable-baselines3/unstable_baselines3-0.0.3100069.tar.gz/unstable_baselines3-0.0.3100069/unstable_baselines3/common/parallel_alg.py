from pettingzoo import ParallelEnv

from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.on_policy_algorithm import OnPolicyAlgorithm

from unstable_baselines3.common.common import conform_act_shape
from unstable_baselines3.common.multi_agent_alg import MultiAgentAlgorithm
from unstable_baselines3.ppo import WorkerPPO


class ParallelAlgorithm(MultiAgentAlgorithm):
    def __init__(self,
                 parallel_env: ParallelEnv,
                 workers,
                 policy=MlpPolicy,
                 DefaultWorkerClass=WorkerPPO,
                 worker_infos=None,
                 **worker_kwargs,
                 ):
        """
        initializes multi agent algorithm with specified workers
        if any agent_ids are unspecified, uses DefaultWorkerClass to initalize them
        Args:
            parallel_env: Pettingzoo ParallelEnv to use
            workers: dict of agentid -> worker
                trainable workers must inherit
                    multi_agent_algs.off_policy:OffPolicyAlgorithm
                    or multi_agent_algs.on_policy:OnPolicyAlgorithm
                untrainable workers must have a get_action (obs -> action) method
            worker_infos: dict of agentid -> (worker info dict)
                worker info dict contains
                    DICT_TRAIN: bool (whether or not to train worker)

            policy: Type of policy to use for stableBaselines algorithm
            DefaultWorkerClass: class to use to initialize workers
            **worker_kwargs: kwargs to use to initializw workers
        """
        super().__init__(
            policy=policy,
            env=parallel_env,
            DefaultWorkerClass=DefaultWorkerClass,
            workers=workers,
            worker_infos=worker_infos,
            **worker_kwargs,
        )

        self.last_observations = dict()
        self.last_infos = dict()

    def learn_episode(self,
                      total_timesteps,
                      number_of_eps=None,
                      strict_timesteps=True,
                      callbacks=None,
                      ):
        """
        learn episode, collects total_timesteps steps then trains
        Args:
            total_timesteps: number of timesteps to collect
            number_of_eps: if specified, overrides total_timesteps, and instead collects this number of episodes
            strict_timesteps: if true, breaks an episode in the middle if timesteps are over
            callbacks:
        Returns: number of collected timesteps
        """
        if callbacks is None:
            callbacks = {agent: None for agent in self.workers}

        # init learn
        local_init_learn_info = dict()
        for agent in self.get_worker_iter(trainable=True, collectable=None):
            init_learn_info = self.workers[agent].init_learn(
                total_timesteps=total_timesteps,
                callback=callbacks[agent],
            )
            local_init_learn_info[agent] = init_learn_info

        # init rollout
        local_init_rollout_info = dict()
        for agent in self.get_worker_iter(trainable=True, collectable=None):
            init_rollout_info = self.workers[agent].init_rollout(
                init_learn_info=local_init_learn_info[agent],
            )
            local_init_rollout_info[agent] = init_rollout_info

        continue_rollout = True
        steps_so_far = 0
        episodes_completed = 0

        while continue_rollout:
            if number_of_eps is not None:
                if episodes_completed >= number_of_eps:
                    continue_rollout = False
            if strict_timesteps and steps_so_far >= total_timesteps:
                continue_rollout = False
            if not continue_rollout:
                break

            if self.reset_env:
                reset_obj = self.env.reset()
                # sometimes the environment does not send infos as a tuple, we must set them manually in this case
                if type(reset_obj) == tuple:
                    self.last_observations, self.last_infos = reset_obj
                else:
                    self.last_observations = reset_obj
                    self.last_infos = {idx: dict() for idx in self.last_observations}
                self.reset_env = False

            # rollout 1 (start of loop)
            local_rollout_1_info = dict()
            for agent in self.get_worker_iter(trainable=True, collectable=None):
                rollout_1_info = self.workers[agent].rollout_1(
                    init_learn_info=local_init_learn_info[agent],
                    init_rollout_info=local_init_rollout_info[agent],
                )
                local_rollout_1_info[agent] = rollout_1_info

            # rollout 2 (middle of loop, action selection)
            actions = dict()
            local_rollout_2_info = dict()
            for agent in self.get_worker_iter(trainable=True, collectable=None):
                act, rollout_2_info = self.workers[agent].rollout_2(
                    obs=self.last_observations[agent],
                    init_learn_info=local_init_learn_info[agent],
                    init_rollout_info=local_init_rollout_info[agent],
                    rollout_1_info=local_rollout_1_info[agent],
                )
                actions[agent] = conform_act_shape(act, self.env.action_space(agent=agent), )
                local_rollout_2_info[agent] = rollout_2_info
            # also handle the untrainable agents
            for agent in self.get_worker_iter(trainable=False, collectable=None):
                if isinstance(self.workers[agent], BaseAlgorithm):
                    act, _ = self.workers[agent].get_action(
                        obs=self.last_observations[agent]
                    )
                    if isinstance(self.workers[agent], OnPolicyAlgorithm):
                        act = act.cpu().numpy()
                else:
                    act = self.workers[agent].get_action(
                        obs=self.last_observations[agent]
                    )
                actions[agent] = conform_act_shape(act, self.env.action_space(agent=agent), )

            self.last_observations, rewards, terminations, truncations, self.last_infos = self.env.step(actions)
            steps_so_far += 1
            truncation = any([t for (_, t) in truncations.items()])
            termination = any([t for (_, t) in terminations.items()])
            term = termination or truncation

            # rollout 3 (end of loop)
            continue_rollout = None
            for agent in self.get_worker_iter(trainable=True, collectable=None):
                rollout_3_info = self.workers[agent].rollout_3(
                    action=actions[agent],
                    new_obs=self.last_observations[agent],
                    reward=rewards[agent],
                    termination=termination,
                    truncation=truncation,
                    info=self.last_infos.get(agent, dict()),
                    init_learn_info=local_init_learn_info[agent],
                    init_rollout_info=local_init_rollout_info[agent],
                    rollout_1_info=local_rollout_1_info[agent],
                    rollout_2_info=local_rollout_2_info[agent],
                )
                continue_rollout = continue_rollout or rollout_3_info.get('continue_rollout', True)
            if continue_rollout is None:
                # no agents are trainable, we should just keep going until the env ends
                continue_rollout = True
            if term:
                # environment terminated and must be reset next time
                self.reset_env = True
                episodes_completed += 1

        # end rollout
        local_end_rollout_info = dict()
        for agent in self.get_worker_iter(trainable=True, collectable=False):
            end_rollout_info = self.workers[agent].end_rollout(
                init_learn_info=local_init_learn_info[agent],
                init_rollout_info=local_init_rollout_info[agent],
                collect_only=False,
            )
            local_end_rollout_info[agent] = end_rollout_info
        for agent in self.get_worker_iter(trainable=True, collectable=True):
            end_rollout_info = self.workers[agent].end_rollout(
                init_learn_info=local_init_learn_info[agent],
                init_rollout_info=local_init_rollout_info[agent],
                collect_only=True,
            )
            local_end_rollout_info[agent] = end_rollout_info

        for agent in self.get_worker_iter(trainable=True, collectable=False):
            self.workers[agent].finish_learn(
                init_learn_info=local_init_learn_info[agent],
                end_rollout_info=local_end_rollout_info[agent],
                collect_only=False,
            )
        for agent in self.get_worker_iter(trainable=True, collectable=True):
            self.workers[agent].finish_learn(
                init_learn_info=local_init_learn_info[agent],
                end_rollout_info=local_end_rollout_info[agent],
                collect_only=True,
            )
        return steps_so_far, episodes_completed
