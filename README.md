bspwm golden-ratio expansion for focused windows, like in the [golden-ratio.el](https://github.com/roman/golden-ratio.el) plugin for emacs

Whenever you focus a window, this script will increase its size considerably (by about 1.6x). Whatever you're working with gets more real estate on the screen. As you interact with different windows, the active one gets expanded.

![Demo](https://github.com/sumeet/golden/raw/master/golden-demo.gif)

Usage:

Stick this in your bspwmrc:

```sh
exec ~/Projects/golden/run.sh &
```

For example, here's my full bspwmrc:

```sh
#!/bin/sh
killall sxhkd
sxhkd &

bspc monitor -d 1 2 3 4 5 6

bspc config border_width 1
bspc config top_padding 43
bspc config window_gap 0

bspc config split_ratio 0.50
bspc config borderless_monocle true
bspc config gapless_monocle true

bspc config pointer_modifier mod1
bspc config pointer_action1 move
bspc config pointer_action2 resize_side
bspc config pointer_action3 resize_corner
bspc config focus_follows_pointer true

bspc rule -a retroarch state=floating
bspc rule -a plasmashell state=floating border=off layer=normal manage=off center=true
bspc rule -a krunner state=floating

exec ~/Projects/golden/run.sh &
```

Bugs, issues and questions all welcome in the Issues section. Thank you!
