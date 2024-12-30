import cv2
import gymnasium as gym
import numpy as np
import tqdm
from gymnasium.utils.save_video import save_video
from stable_baselines3 import PPO

env = gym.make("Ant-v5", render_mode="rgb_array")

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000)

vec_env = model.get_env()
obs = vec_env.reset()

reward_list = []

for i in tqdm.trange(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    rendered = env.render()
    rendered = cv2.cvtColor(rendered, cv2.COLOR_BGR2RGB)
    if i % 100 == 0:
        cv2.imshow("frame", rendered)
        cv2.waitKey(0)
    if done:
        break

    reward_list.append(reward)


# save_video(
#     frames=rendered,
#     video_folder="videos",
#     fps=env.metadata["render_fps"],
#     step_starting_index=0,
#     episode_index=0,
# )
# break

print(f"mean reward: {np.mean(reward_list)}")
