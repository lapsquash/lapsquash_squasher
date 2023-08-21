from bardapi import Bard

from squasher_py.helpers.env import getEnv
from squasher_py.model.utils.types.bard import TBard

env = getEnv()

bard = TBard(Bard(env.BARD_API_KEY))
answer = bard.getAnswer()("この画像は何ですか")
