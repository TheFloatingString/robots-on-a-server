import fastapi
import gymnasium as gym
import numpy as np
import tqdm
import uvicorn
from pydantic import BaseModel
from stable_baselines3 import PPO, A2C, TD3, SAC, DQN
from wonderwords import RandomWord
import random

app = fastapi.FastAPI()

db = dict()


def create_model_name():
    r = RandomWord()
    return f"{r.word(word_max_length=5)}-{r.word(word_max_length=5)}-{r.word(word_max_length=5)}-{random.randrange(100,999)}"


def create_model_item(name, policy, environment):
    return_dict = dict()
    return_dict["name"] = name
    return_dict["policy"] = policy
    return_dict["environment"] = environment
    return return_dict


def run_training(
    environment: str = None, policy: str = None, n_training_epochs: int = None
) -> dict:
    print(environment)
    env = gym.make(environment)

    if policy.upper() == "PPO":
        model = PPO("MlpPolicy", env, verbose=1)
    elif policy.upper() == "A2C":
        model = A2C("MlpPolicy", env, verbose=1)
    elif policy.upper() == "TD3":
        model = TD3("MlpPolicy", env, verbose=1)
    elif policy.upper() == "SAC":
        model = SAC("MlpPolicy", env, verbose=1)
    elif policy.upper() == "DQN":
        model = DQN("MlpPolicy", env, verbose=1)
    elif policy.upper() == "A2C":
        model = A2C("MlpPolicy", env, verbose=1)
    else:
        raise NameError(f"Policy {policy} not yet implemented in roas.")
    model.learn(total_timesteps=n_training_epochs)

    model_name = create_model_name()
    print(model_name)

    model_dict = create_model_item(
        name=model_name, policy=policy, environment=environment
    )

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

    return {
        "model_dict": model_dict,
        "log": {"mean_reward": float(np.mean(reward_list))},
    }


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
    db[res["model_dict"]["name"]] = res["model_dict"]
    return res


if __name__ == "__main__":
    uvicorn.run(app)
