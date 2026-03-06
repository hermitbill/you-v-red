level = {
    'phase_1': {
        'hp_ratio': (0.66, 1.0),
        'movement': 'left_right',
        'helper': False,
        'patterns': [
            ('stack', dict(angle_deg=90, n=3, speed=4, spread=45, spread_rate=1)),
            ('spray', dict(angle_deg=90, n=5, speed=2, spread=45, spread_rate=0.8))
        ]
    },

    'phase_2': { 
        'hp_ratio': (0.33, 0.66),
        'movement': 'stand_still',
        'helper': True,
        'patterns': [
            ('spray', dict(angle_deg=90, n=5, speed=1, spread=60, spread_rate=3)),
            ('spray', dict(angle_deg=90, n=4, speed=2, spread=30, spread_rate=0.8)),
            ('ring', dict(radius=5, n_bullets=24, speed=1, spread_rate=5))
        ]
    },

    'phase_4': {
        'hp_ratio': (0.00, 0.33),
        'movement': 'left_right',
        'helper': False,
        'patterns': [
            ('ring', dict(radius=10, n_bullets=24, speed=3, spread_rate=0.2)),
            ('spray', dict(angle_deg=90, n=7, speed=3, spread=60, spread_rate=0.2)),
        ]
    },
}
