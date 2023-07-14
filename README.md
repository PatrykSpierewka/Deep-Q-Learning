# Deep-Q-Learning
## Game control bot: a reinforcement learning-based project

Reinforcement learning in game control refers to a learning approach where an agent learns to make decisions and take actions in a game environment to maximize a cumulative reward signal. The agent interacts with the game environment, receives feedback in the form of rewards or penalties based on its actions, and uses this feedback to update its decision-making policy.

![flow](https://github.com/PatrykSpierewka/Deep-Q-Learning/assets/101202344/561ceee5-8e50-46df-91c9-50cf6c7681f5)
![equation](https://github.com/PatrykSpierewka/Deep-Q-Learning/assets/101202344/b611711b-d388-4f04-9603-ffa28a1e2685)

# Trained Dino
In the folder "Dinosaur_Game" there is the code to run the game: "Game", the code of the reinforcement learning algorithm: "DQN" and the file with the extension h5 containing the weights of the learned model. The algorithm can be run in two modes:
1. Running the learned model with weights from the file: "model_weights" (commented line 142 - agent.load("model_weights.h5"), uncommented line 218 - agent.save("model_weights.h5")).
2. Model training with saving current weights for each model evaluation (uncommented line 142 - agent.load("model_weights.h5"), commented line 218 - agent.save("model_weights.h5")).
![dino_gif](https://github.com/PatrykSpierewka/Deep-Q-Learning/assets/101202344/780a559b-7a25-4642-bb39-c38b39a76bdf)
![dino_plots](https://github.com/PatrykSpierewka/Deep-Q-Learning/assets/101202344/ce5b4444-543c-4cd6-8bb5-d41337aa9d36)

# Trained Snake
In the folder "Snake_Game" there is the code to run the game: "Game", the code of the reinforcement learning algorithm: "DQN" and the file with the extension h5 containing the weights of the learned model. The algorithm can be run in two modes:
1. Running the learned model with weights from the file: "model_weights" (commented line 160 - agent.load("model_weights.h5"), uncommented line 242 - agent.save("model_weights.h5")).
2. Model training with saving current weights for each model evaluation (uncommented line 160 - agent.load("model_weights.h5"), commented line 242 - agent.save("model_weights.h5")).
![snake_gif](https://github.com/PatrykSpierewka/Deep-Q-Learning/assets/101202344/07a6093b-5785-4959-b5e4-04bcf4e819d2)
![plots_snake](https://github.com/PatrykSpierewka/Deep-Q-Learning/assets/101202344/23b23079-a1ce-43eb-b318-873a36632936)


