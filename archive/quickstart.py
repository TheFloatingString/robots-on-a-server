import gymnasium as gym
import numpy as np
import tqdm
from stable_baselines3 import PPO

env = gym.make("HalfCheetah-v5", render_mode="rgb_array")

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000)

vec_env = model.get_env()
obs = vec_env.reset()

reward_list = []

for i in tqdm.trange(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    reward_list.append(reward)


print(f"mean reward: {np.mean(reward_list)}")
