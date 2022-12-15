"""
===================================
Pan/zoom events of overlapping axes
===================================

Example to illustrate how pan/zoom events of overlapping artists are treated.


The default is the following:

- Axes with a visible patch capture pan/zoom events
- Axes with an invisible patch forward pan/zoom events to axes below
- Twin-axes always trigger with their parent axes
  (irrespective of the patch visibility)


``ax.set_captures_navigation(val)`` can be used to override the
default behaviour:

- ``val=False``: Forward navigation events to axes below
- ``val=True``: Capture navigation events
- ``val="auto"``: Use the default behaviour

"""


import matplotlib.pyplot as plt


def styleax(ax, bg_visible, color, zorder, txt_xy=(.5, .5), txt=None):
    """
    Set relevant axes properties, color axes and add a text to indicate
    patch-visibility zorder.

    Parameters
    ----------
    ax : matplotlib.Axes
        The axes object to style
    bg_visible : bool
        Indicator if the background-patch of the axes should
        be visible or not.
    color : str
        The color to use for the background-patch and/or the
        edgecolor of the axes.
    zorder : int
        The zorder to assign to the axes.
    txt_xy : tuple or None, optional
        The relative position of the label.
        If None, no label will be added.
        The default is (.5,.5).
    txt : str or None, optional
        The text to put on the axis.
        If None, the text indicates patch-visibility and zorder
        as follows:

        >>> "NO patch axes"
        >>> "(zorder=3)   "
    """
    if bg_visible is False:
        ax.patch.set_visible(False)
        for _, s in ax.spines.items():
            s.set_edgecolor(color)
        ax.tick_params(axis='x', colors=color)
        ax.tick_params(axis='y', colors=color)
    else:
        ax.patch.set_facecolor(color)
        for _, s in ax.spines.items():
            s.set_edgecolor(color)

        ax.tick_params(axis='x', colors=color)
        ax.tick_params(axis='y', colors=color)

    ax.set_zorder(zorder)

    if txt is None:
        txt = (f"{'NO' if bg_visible is False else ''} patch axes \n"
               f"at zorder={zorder}")
    if txt_xy:
        ax.text(*txt_xy,
                txt,
                c=color,
                horizontalalignment="center",
                verticalalignment="center",
                bbox=dict(facecolor='w', alpha=0.75),
                fontsize=7)


f, ax = plt.subplots()
f.suptitle("Showcase for pan/zoom events on overlapping axes.")
styleax(ax, True, ".8", 0, (.5, .05))
styleax(ax.twinx(), None, ".8", 0, False)  # a basic twinx

# added axes with background
ax = f.add_axes((.4, .5, .4, .4))
styleax(ax, True, "g", 0, (.5, .85))

# added axes with background and twinx
ax = f.add_axes((.5, .5, .2, .2))
styleax(ax, True, "b", 0)
styleax(ax.twinx(), None, "b", 0, False)

# added axes with NO background and twinx
ax = f.add_axes((.2, .25, .2, .2))
styleax(ax, False, "r", 0)
styleax(ax.twinx(), None, "r", 0, False)

# added axes with NO background on different zorder
ax = f.add_axes((0.05, .1, .55, .7))
styleax(ax, False, "c", 2, (.5, .7))
styleax(ax.twinx(), False, "c", 2, (.5, .7))

# added axes with background and twinx on different zorder
ax = f.add_axes((.5, .25, .2, .2))
styleax(ax, True, "m", 5)
styleax(ax.twinx(), None, "m", 5, False)
# a another joined axes
ax2 = f.add_axes((.8, .25, .15, .15))
styleax(ax2, True, "m", 5)
ax.sharex(ax2)
ax.sharey(ax2)

# ----- override default behaviour
# axes with NO background and force capturing navigation
ax = f.add_axes((.05, .65, .2, .2))
styleax(ax, False, "darkred", 5, txt="Force\ncapture navigation")
ax.set_capture_navigation_events(True)

# axes with background and force forwarding navigation
ax = f.add_axes((.75, .65, .2, .2))
styleax(ax, True, "darkred", 5, txt="Force\nforward navigation")
ax.set_capture_navigation_events(False)

plt.show()
