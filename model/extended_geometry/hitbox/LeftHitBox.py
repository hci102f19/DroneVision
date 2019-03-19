from model.extended_geometry.hitbox.HitBox import HitBox


class LeftHitBox(HitBox):
    def __init__(self, width, height, **kwargs):
        width_top = (width / 2) * kwargs.get('width_top', 0.97)
        width_bottom = (width / 2) * kwargs.get('width_bottom', 0.6)
        height_top = height * (1 - kwargs.get('height_top', 0.6))

        init_geom = [(0, height), (0, height_top), (width_top, height_top), (width_bottom, height)]

        super().__init__(geom=init_geom, **kwargs)
