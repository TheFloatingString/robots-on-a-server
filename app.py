import fastapi
import gymnasium as gym
import numpy as np
import tqdm
import uvicorn
from pydantic import BaseModel
from stable_baselines3 import PPO, A2C

app = fastapi.FastAPI()


def run_training(
    environment: str = None, policy: str = None, n_training_epochs: int = None
) -> dict:
    print(environment)
    env = gym.make(environment, render_mode="rgb_array")

    if policy.upper() == "PPO":
        model = PPO("MlpPolicy", env, verbose=1)
    elif policy.upper() == "A2C":
        model = A2C("MlpPolicy", env, verbose=1)
    # elif policy.upper() == "TRPO":
    #     model = TRPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=n_training_epochs)

    vec_env = model.get_env()
    obs = vec_env.reset()

    reward_list = []

    for i in tqdm.trange(1000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        reward_list.append(reward)
        if i % 100 == 0:
            vec_env.render("human")

    print(f"mean reward: {np.mean(reward_list)}")

    return {"mean_reward": float(np.mean(reward_list))}


class Item(BaseModel):
    environment: str
    policy: str
    n_training_epochs: str


@app.get("/")
async def root():
    return {"data": "RoaS: Robots on a Server"}


@app.post("/api/dev/run")
async def api_dev_run(item: Item):
    print(item.environment)
    res = run_training(
        environment=item.environment,
        policy=item.policy,
        n_training_epochs=int(item.n_training_epochs),
    )
    return res


if __name__ == "__main__":
    uvicorn.run(app)
