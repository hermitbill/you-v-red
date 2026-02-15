# import pygame
# from practice.state import StateMachine

level = {
    'pahse_1': {
        'color': (0, 255, 0),
        'flash_color': (50, 255, 50)
    },
    'pahse_2': {
        'color': (0, 0, 255),
        'flash_color': (50, 50, 255)
    },
    'pahse_3': {
        'color': (255, 0, 0),
        'flash_color': (255, 50, 50)
    },
    'pahse_4': {
        'color': (255, 0, 255),
        'flash_color': (255, 100, 255)
    }
}


level = {
    'pahse_1': {
        'pattern': 'differnt pattern example',
        'movement': 'movement function'
    },
        'pahse_2': {
        'pattern': 'differnt pattern example',
        'movement': 'movement function'
    },
        'pahse_3': {
        'pattern': 'differnt pattern example',
        'movement': 'movement function'
    },
        'pahse_4': {
        'pattern': 'differnt pattern example',
        'movement': 'movement function'
    },
}


level = {
    'phase_1': {
        'hp_ratio': (0.75, 1.0),
        'movement': 'hover',
        'patterns': [
            ('ring', dict(radius=20, n_bullets=12, speed=1, spread_rate=0.8)),
        ]
    },

    'phase_2': {
        'hp_ratio': (0.50, 0.75),
        'movement': 'strafe',
        'patterns': [
            ('spray', dict(angle_deg=90, n=5, speed=2, spread=45, spread_rate=0.3)),
        ]
    },

    'phase_3': {
        'hp_ratio': (0.25, 0.50),
        'movement': 'dash',
        'patterns': [
            ('stack', dict(angle_deg=90, n=4, speed=4, spread_rate=0.5)),
        ]
    },

    'phase_4': {
        'hp_ratio': (0.00, 0.25),
        'movement': 'rage',
        'patterns': [
            ('ring', dict(radius=10, n_bullets=24, speed=3, spread_rate=0.2)),
            ('spray', dict(angle_deg=90, n=7, speed=3, spread=60, spread_rate=0.2)),
        ]
    },
}
