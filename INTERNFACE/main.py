import eel

eel.init('web')


@eel.expose



eel.start('main.html', size=(800, 800), port=80, cmdline_args=['--start-fullscreen'])