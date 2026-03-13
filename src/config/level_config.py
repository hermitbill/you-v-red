from components.level_eng import *

EVENTS = [
    SpawnEvent(
    trigger=1600,
    enemy_type="grunt",
    size=(30,20),
    hp=35,
    formation=StraightDownFormation(start_pos=(200, -150), stop_y=None, spacing=40, speed=0.5),
    count=1,
    patterns=[
        ('spiral', dict(n=3, spread_rate=0.2, speed=1.5)),
        ('directed', dict(n=3, spread_rate=2, speed=2)),
        ('ring', dict(n_bullets=5, speed=1.5, spread_rate=1))
    ]
),
SpawnEvent(
    trigger=1400,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=StraightDownFormation(start_pos=(230, -150), stop_y=None, spacing=40, speed=0.5),
    count=3,
    patterns=[('directed', dict(n=3, spread_rate=1.5, speed=1.5))]
),
SpawnEvent(
    trigger=1200,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=StraightDownFormation(start_pos=(200, -150), stop_y=None, spacing=40, speed=0.5),
    count=2,
    patterns=[('ring', dict(n_bullets=5, speed=1.5, spread_rate=1))]
),
SpawnEvent(
    trigger=800,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=DiagonalFormation(
        start_pos=(450, -150), spacing=60, angle_deg=135, speed=0.5
    ),
    count=5,
    patterns=[('directed', dict(n=1, spread_rate=2, speed=1.5))]
),
SpawnEvent(
    trigger=600,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=RotationCircleFormation(
        center=(200 // 2, -100),
        radius=50,
        count=5,
        rotation_speed=2,
        drift_velocity=(0, 15),
    ),
    count=5,
    patterns=[('spray', dict(angle_deg=90, n=3, speed=1.5, spread=25, spread_rate=2))]
),
SpawnEvent(
    trigger=400,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=RotationCircleFormation(
        center=(400 // 2, -100),
        radius=50,
        count=5,
        rotation_speed=2,
        drift_velocity=(0, 15),
    ),
    count=5,
    patterns=[('spray', dict(angle_deg=90, n=2, speed=1.5, spread=25, spread_rate=2))]
),
SpawnEvent(
    trigger=150,
    enemy_type="grunt",
    size=(30,20),
    hp=35,
    formation=StraightDownFormation(start_pos=(180, -150), stop_y=None, spacing=40, speed=0.5),
    count=1,
    patterns=[
        ('spiral', dict(n=2, spread_rate=0.2, speed=1.5)),
        ('directed', dict(n=1, spread_rate=2, speed=2))
    ]
),
SpawnEvent(
    trigger=200,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=ZigZagFormation(
        start_pos=(250,-150),
        spacing=20,
        speed=2
    ),
    count=3,
    patterns=[
        ('stack', dict(angle_deg=180, n=1, spread_rate=0.8, speed=1.5)),
    ]
),
    SpawnEvent(
    trigger=150,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=UpDownFormation(
        start_pos=(-150,180), # x,y
        spacing=20,
        speed=2,
        direction='left-right'
    ),
    count=5,
    patterns=[
        ('directed', dict(n=1, spread_rate=2, speed=1.5)),
    ]
),
SpawnEvent(
    trigger=80,
    enemy_type="grunt",
    size=(10,10),
    hp=5,
    formation=UpDownFormation(
        start_pos=(-150,180), # x,y
        spacing=20,
        speed=2,
        direction='down'
    ),
    count=5,
    patterns=[
        ('directed', dict(n=1, spread_rate=2, speed=1.5)),
    ]
),
]

# # ZigZagFormation
# # UpDownFormation
# # RotationCircleFormation
# # StraightDownFormation
# # DiagonalFormation
