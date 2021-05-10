import datetime as dt
import random


class BaseBandit:
    def __init__(self, probs):
        self.probs = probs
        self.arms = probs.keys()

    @property
    def options(self):
        return list(self.probs.keys())

    def pull(self, arm):
        if arm not in self.options:
            return -1
        return 1 if random.random() < self.probs[arm] else 0


class Casino:
    def __init__(self, bandits, passwords=None, start_amount=5000, redis=None):
        self.bandits = bandits
        self.passwords = passwords
        self._redis = redis
        self._start_amount = start_amount

    def reset(self):
        for user in self.passwords.keys():
            for bandit in self.bandits.keys():
                self._redis.hmset(
                    f"users:{user}:{bandit}", {"points": 0, "coins": self._start_amount}
                )

    def call(self, user, password, bandit, arm):
        return (
            self.credential_check(user, password)
            or self.casino_check(user, bandit, arm)
            or self.attempt(user, bandit, arm)
        )

    @property
    def state(self):
        return {
            bandit: {
                user: self._redis.hgetall(f"users:{user}:{bandit}")
                for user in self.passwords.keys()
            }
            for bandit in self.bandits.keys()
        }

    def credential_check(self, user, password):
        if user not in self.passwords.keys():
            return {"status": "user not in config"}
        if self.passwords[user] != password:
            return {"status": "incorrect password"}
        return None

    def casino_check(self, user, bandit, arm):
        if bandit not in self.bandits.keys():
            return {"status": "bandit does not exist"}

        if arm not in self.bandits[bandit].arms:
            return {"status": f"arm {arm} does not exist in bandit {bandit}"}
        return None

    def attempt(self, user, bandit, arm):
        arm_value = self.bandits[bandit].pull(arm)

        coins = self._redis.hget(f"user:{user}:{bandit}", "coins")
        if coins == 0:
            return {"status": "out of coins!"}

        self._redis.hincrby(f"users:{user}:{bandit}", "coins", -1)
        self._redis.hincrby(f"users:{user}:{bandit}", "points", arm_value)

        return {
            "timestamp": str(dt.datetime.now()),
            "bandit": bandit,
            "arm": arm,
            "status": "received",
            "value": arm_value,
        }
