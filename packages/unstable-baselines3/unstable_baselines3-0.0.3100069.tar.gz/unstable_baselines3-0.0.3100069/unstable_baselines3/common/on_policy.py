import numpy as np
import torch
from gymnasium import spaces

from stable_baselines3.common.utils import obs_as_tensor
from stable_baselines3.common.buffers import DictRolloutBuffer

from unstable_baselines3.common.common import conform_shape, conform_act_shape


class OnPolicy:
    reset_rollout = True

    def init_learn(self,
                   callback,
                   total_timesteps,
                   tb_log_name: str = "run",
                   reset_num_timesteps: bool = False,
                   progress_bar: bool = False,
                   log_interval=4,
                   ):
        self.iteration = 0
        total_timesteps, callback = self._setup_learn(
            total_timesteps,
            callback,
            reset_num_timesteps,
            tb_log_name,
            progress_bar,
        )

        callback.on_training_start(locals(), globals())

        assert self.env is not None, "You must set the environment before calling learn()"

        init_learn_info = {'callback': callback,
                           'log_interval': log_interval,
                           'total_timesteps': total_timesteps,
                           }
        return init_learn_info

    def init_rollout(self,
                     init_learn_info
                     ):
        callback = init_learn_info.get('callback')

        # Switch to eval mode (this affects batch norm / dropout)
        self.policy.set_training_mode(False)

        if self.reset_rollout:
            # if this isnt true, we have untrained examples in the buffer, and should continue adding to it
            self.num_collected_steps = 0
            self.rollout_buffer.reset()
            self.reset_rollout = False
        if self.use_sde:
            self.policy.reset_noise(self.env.num_envs)

        self.starting_steps = self.num_collected_steps
        callback.on_rollout_start()
        return None

    def rollout_1(self,
                  init_learn_info,
                  init_rollout_info,
                  ):
        # while should_collect_more_steps(train_freq, num_collected_steps, num_collected_episodes):
        if self.use_sde and self.sde_sample_freq > 0 and self.num_collected_steps%self.sde_sample_freq == 0:
            # Sample a new noise matrix
            self.policy.reset_noise(self.env.num_envs)
        return None

    def rollout_2(self,
                  obs,
                  init_learn_info,
                  init_rollout_info,
                  rollout_1_info,
                  ):
        with torch.no_grad():
            actions, (values, log_probs) = self.get_action(obs=obs, )
            actions = conform_act_shape(actions, act_space=self.action_space)
        actions = actions.cpu().numpy()

        # Rescale and perform action
        clipped_actions = actions

        if isinstance(self.action_space, spaces.Box):
            if self.policy.squash_output:
                # Unscale the actions to match env bounds
                # if they were previously squashed (scaled in [-1, 1])
                clipped_actions = self.policy.unscale_action(clipped_actions)
            else:
                # Otherwise, clip the actions to avoid out of bound error
                # as we are sampling from an unbounded Gaussian distribution
                clipped_actions = np.clip(actions, self.action_space.low, self.action_space.high)

        return clipped_actions, (values, log_probs)

    def rollout_3(self,
                  action,
                  new_obs,
                  reward,
                  termination,
                  truncation,
                  info,
                  init_learn_info,
                  init_rollout_info,
                  rollout_1_info,
                  rollout_2_info,
                  rollout_buffer=None,
                  ):
        if rollout_buffer is None:
            rollout_buffer = self.rollout_buffer
        values, log_probs = rollout_2_info
        callback = init_learn_info.get('callback')
        log_interval = init_learn_info.get('log_interval')

        self.num_timesteps += self.env.num_envs

        # Give access to local variables
        callback.update_locals(locals())
        callback.on_step()
        # Only stop training if return value is False, not when it is None.
        # if not callback.on_step():
        #    return RolloutReturn(num_collected_steps*env.num_envs, num_collected_episodes, continue_training=False)
        dones = np.array([termination or truncation])
        # Retrieve reward and episode length if using Monitor wrapper
        self._update_info_buffer(info, dones=dones)

        self.num_collected_steps += 1

        if isinstance(self.action_space, spaces.Discrete):
            # Reshape in case of discrete action
            action = action.reshape(-1, 1)

        new_obs = conform_shape(new_obs, self.observation_space)
        # Handle timeout by bootstraping with value function
        # see GitHub issue #633

        if (
                dones[0]
                and info.get("terminal_observation") is not None
                and info.get("TimeLimit.truncated", False)
        ):
            terminal_obs = self.policy.obs_to_tensor(info["terminal_observation"])[0]
            with torch.no_grad():
                terminal_value = self.policy.predict_values(terminal_obs)[0]  # type: ignore[arg-type]
            reward += self.gamma*terminal_value

        if rollout_buffer.full:
            # this should probably not happen
            # if it does, we should start collecting more recent samples
            rollout_buffer.pos = 0
        rollout_buffer.add(
            self._last_obs,  # type: ignore[arg-type]
            action,
            reward,
            self._last_episode_starts,  # type: ignore[arg-type]
            values,
            log_probs,
        )
        self._last_obs = conform_shape(new_obs, obs_space=self.observation_space)  # type: ignore[assignment]
        self._last_episode_starts = dones
        # if current rollout size is less than max rollout size, continue rollout
        return {
            'continue_rollout': not rollout_buffer.full,
            'steps_so_far': self.num_collected_steps - self.starting_steps,
        }

    def get_action(self, obs):

        self._last_obs = conform_shape(obs, self.observation_space)
        # Convert to pytorch tensor or to TensorDict
        # TODO: why for image spaces does this work
        obs_tensor = obs_as_tensor(self._last_obs, self.device)
        if isinstance(obs_tensor, dict):
            pass
        else:
            obs_tensor = obs_tensor.unsqueeze(0)
        actions, values, log_probs = self.policy(obs_tensor)
        return actions, (values, log_probs)

    def potential_train_from_rollout(self, init_learn_info, collect_only):
        if collect_only: return False
        if self.rollout_buffer.full:
            callback = init_learn_info.get('callback')
            log_interval = init_learn_info.get('log_interval')
            total_timesteps = init_learn_info.get('total_timesteps')
            dones = self._last_episode_starts

            with torch.no_grad():
                # Compute value for the last timestep
                values = self.policy.predict_values(
                    obs_as_tensor(self._last_obs, self.device))  # type: ignore[arg-type]

            self.rollout_buffer.compute_returns_and_advantage(last_values=values, dones=dones)

            callback.update_locals(locals())

            callback.on_rollout_end()

            self.iteration += 1
            self._update_current_progress_remaining(self.num_timesteps, total_timesteps)

            # Display training infos
            if log_interval is not None and self.iteration%log_interval == 0:
                assert self.ep_info_buffer is not None
                self._dump_logs(self.iteration)

            self.train()
            # we just trained on the buffer, so we should reset the buffer time we initialize an episode
            self.reset_rollout = True
            return True
        return False

    def end_rollout(self,
                    init_learn_info,
                    init_rollout_info,
                    rollout_buffer=None,
                    collect_only=False,
                    ):
        if rollout_buffer is None:
            rollout_buffer = self.rollout_buffer

        if not rollout_buffer.full:
            # if we have not collected enough training steps to fill rollout, continue
            return {'num_collected_steps': self.num_collected_steps - self.starting_steps,
                    'rollout_filled': False,
                    }
        self.potential_train_from_rollout(init_learn_info=init_learn_info, collect_only=collect_only, )
        return {'num_collected_steps': self.num_collected_steps - self.starting_steps,
                'rollout_filled': True,
                }

    def finish_learn(self, init_learn_info, end_rollout_info, collect_only=False, ):
        callback = init_learn_info.get('callback')
        callback.on_training_end()

    def update_from_buffer(self, local_buffer):
        updated = False
        init_learn_info = self.init_learn(callback=None,
                                          total_timesteps=local_buffer.size()
                                          )
        init_rollout_info = self.init_rollout(init_learn_info=init_learn_info)
        if local_buffer.full:
            pos_0 = (local_buffer.pos + 1)%local_buffer.buffer_size
        else:
            pos_0 = 0
        for i in range(local_buffer.size()):
            pos = (i + pos_0)%local_buffer.buffer_size
            if isinstance(local_buffer, DictRolloutBuffer):
                assert isinstance(self.rollout_buffer, DictRolloutBuffer)
                obs = {key: local_buffer.observations[key][pos]
                       for key in local_buffer.observations}
            else:
                obs = local_buffer.observations[pos]
            action = local_buffer.actions[pos]
            reward = local_buffer.rewards[pos]
            episode_start = local_buffer.episode_starts[pos]
            value = torch.tensor(local_buffer.values[pos])
            log_prob = torch.tensor(local_buffer.log_probs[pos])
            if self.reset_rollout:
                self.rollout_buffer.reset()
                self.reset_rollout = False
            self.rollout_buffer.add(
                obs=obs,
                action=action,
                reward=reward,
                episode_start=episode_start,
                value=value,
                log_prob=log_prob,
            )
            updated = updated or self.potential_train_from_rollout(init_learn_info=init_learn_info, collect_only=False)
        end_rollout_info = self.end_rollout(init_learn_info=init_learn_info, init_rollout_info=init_rollout_info)
        self.finish_learn(init_learn_info=init_learn_info, end_rollout_info=end_rollout_info)
        return updated
