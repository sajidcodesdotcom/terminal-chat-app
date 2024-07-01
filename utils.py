
def animate_text(type, text):
    effect = type(text)
    effect.effect_config.merge = True
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)

