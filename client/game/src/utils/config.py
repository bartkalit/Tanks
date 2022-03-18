class Config:
    player = {
        'speed': {
            'drive': {
                'forward': 120,
                'backward': 70
            },
            'rotate': 80
        },
        'tank': {
            'scale': 0.7,
            'magazine': 5,
            'reload_bullet': 3,
            'reload_magazine': 10
        },
        'lives': 3
    }

    game = {
        'fps': 60
    }

    bullet = {
        'speed': 180,
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
