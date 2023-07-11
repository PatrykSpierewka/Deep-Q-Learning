from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import random
import numpy as np
from collections import deque
import os
from Game import Dinosaur

clear = lambda: os.system('cls')

env = Dinosaur()

state_size = 4
action_size = 3

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.buffer_size = 3000
        self.memory = deque(maxlen=self.buffer_size)
        self.gamma = 0.975  # future discount
        self.epsilon = 1  # epsilon greedy
        self.epsilon_decay = 0.99994
        self.epsilon_min = 0.01
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.target_model.set_weights(self.model.get_weights())
        self.target_copy = 1000

    def build_model(self):
        model = Sequential()
        model.add(Dense(48, input_dim=self.state_size, activation='relu'))
        model.add(Dense(48, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=0.001))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # save memory

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randint(0, action_size - 1)
        act_values = self.model.predict(state, verbose=0)  # for every input from action_size
        return np.argmax(act_values[0])

    def replay(self, trainings):
        batch_size = 32
        batch = random.sample(self.memory, batch_size)

        state_batch = np.zeros((batch_size, state_size))
        next_state_batch = np.zeros((batch_size, state_size))
        action_batch, reward_batch, done_batch = [], [], []

        for i in range(batch_size):
            state_batch[i] = batch[i][0]
            action_batch.append(batch[i][1])
            reward_batch.append(batch[i][2])
            next_state_batch[i] = batch[i][3]
            done_batch.append(batch[i][4])

        q = self.model.predict(state_batch)  # Q value for both actions for all states from the batch
        q_target = self.target_model.predict(next_state_batch)  # Q values for both actions for all future states from the batch

        for i in range(batch_size):
            q_bellman = reward_batch[i]
            if not done_batch[i]:
                q_bellman = reward_batch[i] + self.gamma * np.amax(q_target[i])

            q[i][action_batch[i]] = q_bellman  # substitute q value for action taken by the value from Bellman equation

        self.model.fit(state_batch, q, epochs=1, batch_size=batch_size, verbose=0)

        if trainings % self.target_copy == 0:
            self.target_model.set_weights(self.model.get_weights())

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)
        self.target_model.load_weights(name)


class Evaluator:
    mode = False

    def __init__(self):
        self.score_hist = []  # history of results during evaluation
        self.avg_score_hist = []  # history of all average results
        self.steps_target = 1500  # number of frames during the evaluation

        self.steps = 0  # step counter

        self.override = True  # overwriting existing files

        self.q_set_collected = False  # collecting data for evaluating the average Q
        self.q_set_size = 1500  # number of states to remember
        self.avg_q_hist = []

    def get_q_set(self, buffer):
        ran_mem = random.sample(buffer, self.q_set_size)
        q_set = np.zeros((self.q_set_size, state_size))

        for i in range(self.q_set_size):
            q_set[i] = ran_mem[i][0]

        self.q_set = q_set
        self.q_set_collected = True

    def evaluate_avg_q(self):
        q = agent.model.predict(self.q_set)  # returns Q for each action
        res = np.average(np.max(q, axis=1))  # average(max Q)
        self.avg_q_hist.append(res)

    def evaluate_score(self):
        sum = 0
        sum_t = 0
        for i in range(len(self.score_hist)):
            sum += self.score_hist[i]

        self.avg_score_hist.append(sum / len(self.score_hist))
        self.score_hist = []

        for i in range(len(train_score_hist)):
            sum_t += train_score_hist[i]

        if len(train_score_hist) != 0:
            train_score_avg_hist.append(sum_t / len(train_score_hist))
        else:
            train_score_avg_hist.append(0)

trainings = 0
epoch_size = 2000

agent = DQNAgent(state_size, action_size)
agent.load("model_weights.h5")  # Loading trained weights

ev = Evaluator()
train_score_hist = deque(maxlen=10)
train_score_avg_hist = []


for e in range(0, 10000):
    state = env.reset()
    state = np.reshape(state, [1, state_size])

    env.done = 0
    score = 0

    for time in range(0, 100000):
        clear()
        print("Episode: " + str(e))
        print("Trainings: " + str(trainings))
        print("Epsilon " + str(agent.epsilon))
        print("Evaluation: " + str(ev.mode))

        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        reward = reward if not done else -1

        score += reward
        next_state = np.reshape(next_state, [1, state_size])

        if not Evaluator.mode:
            agent.remember(state, action, reward, next_state, done)

        state = next_state

        if trainings % epoch_size == 0 and len(agent.memory) == agent.buffer_size:
            if not Evaluator.mode:
                if not ev.q_set_collected:
                    ev.get_q_set(agent.memory)
                ev.evaluate_avg_q()
                Evaluator.mode = True
                print("EWALUACJA")
                ev.prev_epsilon = agent.epsilon
                agent.epsilon = agent.epsilon_min
                break
            elif ev.steps == ev.steps_target:
                if len(ev.score_hist) == 0:
                    ev.score_hist.append(score)
                Evaluator.mode = False
                ev.steps = 0
                ev.evaluate_score()
                print("Koniec ewaluacji")
                ev.save()
                agent.epsilon = ev.prev_epsilon
                agent.replay(trainings)
                trainings += 1
                break

            else:
                ev.steps += 1

        if len(agent.memory) == agent.buffer_size and not Evaluator.mode:
            agent.replay(trainings)
            print("replay")
            trainings += 1

        if done:
            if Evaluator.mode:
                ev.score_hist.append(score)
                print("Appended score")
                print(score)

            else:
                if len(agent.memory) == agent.buffer_size and not Evaluator.mode:
                    print('score:' + str(score))
                    train_score_hist.append(score)
            break

    #agent.save("model_weights.h5")