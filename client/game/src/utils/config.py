class Config:
    player = {
        'speed': {
            'drive': {
                'forward': 40,
                'backward': 100
            },
            'rotate': 80
        },
        'tank': {
            'scale': 0.7,
            'magazine': 8,
            'reload_bullet': 2,
            'reload_magazine': 1
        },
        'lives': 20
    }

    game = {
        'fps': 60
    }

    bullet = {
        'speed': 80,
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
