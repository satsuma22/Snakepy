# Snakepy

## Table of Contents
- [About the Project](#about-the-project)
- [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
- [Configuration](#configuration)

## About the Project
Snakepy is an agent that learns to play the game Snake using the genetic algorithm. You can also play the game yourself :)

## Installing Dependencies
The application has only two external dependencies, `pygame` and `numpy`. These can installed with the help of the `requirements.txt` file. Use the following command to install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage
For playing the game and watching the agent play the game, run the main application by using the following command:
```bash
python main.py
```
Clicking on `Play` launches the game for you to play. Use `w` `s` `a` `d` or the arrow keys to move the snake. Clicking on `Genetic Algorithm` loads the trained agent from a save file (if present). You can then watch the agent play the game. Note: Clicking `Genetic Algorithm` randomly loads one agent from the latest generation of population. To randomly select another agent, press `ESC` and click on `Genetic Algorithm` again.

For training the agent, use the script `train_script.py`. While running the script from command line, a second argument can be provided, which specifies the number of generations of training.
```bash
python train_script.py [number_of_generations]
```
