from bark.ui.ui import Render

def test_break_up_text():
    render = Render()
    print('\n')
    line = render._break_up_text("qwer asdf zxcv tyui ghjk bnm, qwer asdf zxcv tyi ghk bnm,", 10, 4)
    print(line)
