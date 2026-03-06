from components.level_eng import *

EVENTS = [
    SpawnEvent(
        trigger=100,
        enemy_type="grunt",
        formation=DiagonalFormation(
            start_pos=(450, -150), spacing=60, angle_deg=135, speed=30
        ),
        count=5,
        patterns=[('directed', dict(n=1, spread_rate=2, speed=10))]
    ),
    SpawnEvent(
        trigger=50,
        enemy_type="grunt",
        formation=StraightDownFormation(start_pos=(150, -100), stop_y=50, spacing=40, speed=30),
        count=1,
        patterns=[('spray', dict(angle_deg=90, n=4, speed=10, spread=20, spread_rate=2))] # 60fps
    ),
        SpawnEvent(
        trigger=3000,
        enemy_type="grunt",
        formation=StraightDownFormation(start_pos=(150, -100), stop_y=None, spacing=40, speed=30),
        count=1,
        patterns=[('ring', dict(n_bullets=6, speed=10, spread_rate=1))]
    ),
        SpawnEvent(
        trigger=2000,
        enemy_type="grunt",
        formation=StraightDownFormation(start_pos=(150, -100), stop_y=None, spacing=40, speed=30),
        count=1,
        patterns=[('directed', dict(n=3, spread_rate=2, speed=10))]
    ),
    SpawnEvent(
        trigger=1400,
        enemy_type="grunt",
        formation=RotationCircleFormation(
            center=(400 // 2, -100),
            radius=50,
            count=5,
            rotation_speed=2,
            drift_velocity=(0, 15),
        ),
        count=5,
        patterns=[('spray', dict(angle_deg=90, n=3, speed=10, spread=25, spread_rate=2))]
    ),
        SpawnEvent(
        trigger=3000,
        enemy_type="grunt",
        formation=StraightDownFormation(start_pos=(10, -100), stop_y=None, spacing=30, speed=10),
        count=3,
        patterns=[('stack', dict(angle_deg=0, speed=10, n=2 ,spread_rate=1))]
    ),
        
        SpawnEvent(
        trigger=3000,
        enemy_type="grunt",
        formation=StraightDownFormation(start_pos=(290, -100), stop_y=None, spacing=30, speed=10),
        count=3,
        patterns=[('stack', dict(angle_deg=180, speed=10, n=2 ,spread_rate=1))]
    ),
]

