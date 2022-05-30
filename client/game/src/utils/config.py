class Config:
    player = {
        'speed': {                      # normal | simulation
            'drive': {
                'forward': 560,         # 70     | 560
                'backward': 720         # 90     | 720
            },
            'rotate': 1200              # 150    | 1200
        },
        'tank': {
            'scale': 0.7,
            'magazine': 8,
            'reload_bullet': 2,
            'reload_magazine': 4
        },
        'lives': 3
    }

    game = {
        'fps': 200
    }

    bullet = {
        'speed': 880,                   # 120    | 880
        'scale': 0.09
    }

    screen = {
        'resolution': {
            'width': 800,
            'height': 800
        },
        'stat_bar': 80
    }

    rewards = {
        'hit': 50,
        'kill': 200
    }
