"""Chart-level checks: real objects inside the allowed band, labels clear of each other."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pytest  # noqa: E402
from matplotlib.text import Text  # noqa: E402

from allowed_universe import charts, engine  # noqa: E402

SPEC_CHARTS = [m for m in charts.all_charts() if hasattr(m, "spec")]
ALL = charts.all_charts()


@pytest.mark.parametrize("mod", SPEC_CHARTS, ids=lambda m: m.NAME)
def test_objects_inside_hard_bounds(mod):
    assert engine.violations(mod.spec()) == []


@pytest.mark.parametrize("mod", SPEC_CHARTS, ids=lambda m: m.NAME)
def test_every_category_has_a_style(mod):
    spec = mod.spec()
    for cat in spec.objects["category"].unique():
        assert cat in spec.categories, cat


@pytest.mark.parametrize("mod", SPEC_CHARTS, ids=lambda m: m.NAME)
def test_labels_do_not_overlap(mod):
    fig = engine.render(mod.spec())
    ax = fig.axes[0]
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    boxes = [Text.get_window_extent(t, r) for t in ax.texts if getattr(t, "_placement_score", None) is not None]
    assert boxes
    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            assert not a.overlaps(b)
    plt.close(fig)


@pytest.mark.parametrize("mod", ALL, ids=lambda m: m.NAME)
def test_renders(mod, tmp_path):
    fig = engine.render(mod.spec()) if hasattr(mod, "spec") else mod.render()
    engine.save(fig, mod.NAME, outdir=tmp_path)
    assert (tmp_path / f"{mod.NAME}.png").stat().st_size > 10_000
    assert (tmp_path / f"{mod.NAME}.pdf").stat().st_size > 5_000
