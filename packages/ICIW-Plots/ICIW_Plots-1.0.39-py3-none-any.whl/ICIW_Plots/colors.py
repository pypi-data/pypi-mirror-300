import matplotlib as mpl
import colorsys
import numpy as np
from cycler import cycler, Cycler


def adjacent_colors(
    base_color: tuple[float, float, float],
    n: int = 5,
    phi: int = 15,
) -> list[tuple[float, float, float],]:

    base_H, L, S = colorsys.rgb_to_hls(*base_color)
    base_H *= 360
    colors = []

    iseven = lambda x: not (x // 2)

    if iseven(n):
        raise ValueError(
            "Adjacent color schemes only work for an odd number of colors."
        )

    n_low = (n - 1) / 2
    phi_low = -n_low * phi
    phis = np.linspace(phi_low, -phi_low, n, endpoint=True)

    for i in phis:
        H = (base_H + i) % 360
        color = colorsys.hls_to_rgb(H / 360, L, S)
        colors.append(color)
    return colors


def adjacent_cycler(
    base_color: tuple[float, float, float],
    n: int = 5,
    phi: int = 15,
) -> Cycler:
    _colors = adjacent_colors(base_color, n, phi)
    _cycler = cycler(color=_colors)
    return _cycler


crimson_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 163 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 38 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 56 / 256, 1.0],
    ],
}

cerulean_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 38 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 84 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 124 / 256, 1.0],
    ],
}

kellygreen_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 86 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 170 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 28 / 256, 1.0],
    ],
}

flame_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 233 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 109 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 7 / 256, 1.0],
    ],
}

drab_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 169 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 162 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 141 / 256, 1.0],
    ],
}

CRIMSON = (163 / 256, 38 / 256, 56 / 256)
CERULEAN = (38 / 256, 84 / 256, 124 / 256)
KELLYGREEN = (86 / 256, 170 / 256, 28 / 256)
FLAME = (233 / 256, 109 / 256, 7 / 256)
DRAB = (169 / 256, 162 / 256, 141 / 256)

crimson_cm = mpl.colors.LinearSegmentedColormap("crimson", crimson_dict)
cerulean_cm = mpl.colors.LinearSegmentedColormap("cerulean", cerulean_dict)
kellygreen_cm = mpl.colors.LinearSegmentedColormap("kellygreen", kellygreen_dict)
flame_cm = mpl.colors.LinearSegmentedColormap("flame", flame_dict)
drab_cm = mpl.colors.LinearSegmentedColormap("drab", drab_dict)

crimson_adjacent = adjacent_colors(CRIMSON)
cerulean_adjacent = adjacent_colors(CERULEAN)
kellygreen_adjacent = adjacent_colors(KELLYGREEN)
flame_adjacent = adjacent_colors(FLAME)
drab_adjacent = adjacent_colors(DRAB)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(layout="constrained")

    fig.colorbar(
        mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=flame_cm),
        ax=ax,
        orientation="vertical",
        label="a colorbar label",
    )

    plt.show()
