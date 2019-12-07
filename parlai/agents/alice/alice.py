#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Agent uses the Free Alice AIML interpreter to answer..
"""

import aiml
import os

from parlai.core.agents import Agent


class AliceAgent(Agent):
    """
    Agent returns the Alice AIML bot's reply to an observation.

    This is a strong rule-based baseline.
    """

    def __init__(self, opt, shared=None):
        """
        Initialize this agent.
        """
        super().__init__(opt)
        self.id = 'Alice'
        self.kern = None
        self.load_alice()

    def load_alice(self):
        self.kern = aiml.Kernel()
        self.kern.verbose(False)
        self.kern.setTextEncoding(None)
        chdir = os.path.join(aiml.__path__[0], 'botdata', 'alice')
        self.kern.bootstrap(
            learnFiles="startup.xml", commands="load alice", chdir=chdir
        )

    def get_alice_response(self, obs):
        return self.kern.respond(obs)

    def act(self):
        """
        Generate response to last seen observation.

        Replies with a message from using the Alice bot.

        :returns: message dict with reply
        """

        obs = self.observation
        if obs is None:
            return {'text': 'Nothing to reply to yet.'}

        reply = {}
        reply['id'] = self.getID()
        query = obs.get('text', "I don't know")
        reply['text'] = self.get_alice_response(query)

        return reply
