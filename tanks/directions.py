from pygame import Vector2
NONE = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4


def direction_to_vector(direction: int, speed: float = 1) -> Vector2:
    """방향을 벡터로 변환"""
    if direction == NORTH:
        return Vector2(0, -speed)
    elif direction == EAST:
        return Vector2(speed, 0)
    elif direction == SOUTH:
        return Vector2(0, speed)
    elif direction == WEST:
        return Vector2(-speed, 0)
    elif direction is None:
        return Vector2(0, 0)
    else:
        raise ValueError('Direction is out of range')

