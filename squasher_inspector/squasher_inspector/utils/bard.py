from bardapi import Bard

from squasher_core.helpers.env import getEnv
from squasher_core.model.utils.types.bard import TBard

env = getEnv()

bard = TBard(Bard(env.BARD_API_KEY))
answer = bard.getAnswer()("この画像は何ですか")
