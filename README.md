# YOU vs <span style=color:red;>RED</span>

_A top-down shooter boss fight built in Pygame._

## About the Game

You control a lone player dodging waves of bullets fired by Red and his
helpers. YOU vs RED draws inspiration from bullet-hell acrade games
without fully adpoting the genre\'s design rules.

### References used:

- The Electric Underground (background into the genre)
- Andrew Fan (bullet design & mechanics)

## Survive

<p align="center">
  <img src="docs/gifs/survive.gif" alt="Dodge the wave of bullets">
</p>

Survive waves of bullets. The game uses bullets pooling for perforamance
and consistency projectile behavior. Red and his helpers run on a
modular system with independent movement, bullet pattern and combat
components, enabling customization.

## Shoot

<p align="center">
  <img src="docs/gifs/shoot.gif" alt="shoot'em up">
</p>

Defeat Red and his helpers by shooting them. The game uses clear visual
feedback to strengthen game feel. Squash-and-stretch animations
emphasize shooting, procedural blood particles respond to hits, and
collision sparks mark impacts instantly.

## Controls

- Move: Arrow keys
- Attack: Spacebar
- Quit: Window

## Running the Game

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Project Status

You vs Red is a **work in progress**.

## Changelog

### v1.0

intial fork
