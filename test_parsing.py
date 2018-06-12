from CMSchecker import Text, TextLine

doc = r"""\section{Corrections for $\PT > 50 \GeV$}

I hear the drums \echoing{tonight}
But she hears only whispers of some quiet conversation
She's coming in, $12:30$ flight
The moonlit wings reflect the stars that guide me towards salvation
I stopped an old man along the way
Hoping to find some long forgotten words or ancient melodies
He turned to me as if to say, "Hurry boy, it's waiting there for you"
\drums{yes}\drums{big}
\begin{chorus}
\begin{center}
    It's gonna take a lot to take me away from you
    There's nothing that a $100$ men or more could ever do
    I bless the rains down in Africa
    Gonna take some time to do the things we never had
    \caption{Bah bah}\label{chorus1}
\end{center}
\end{chorus}

"""


t = Text(doc.splitlines())

def test_inline_maths():
    math_lines = t.iter_inline_maths()
    expect = [
        TextLine(line_num=1, char_num_start=1, text=r"\PT > 50 \GeV"),
        TextLine(line_num=5, char_num_start=1, text="12:30"),
        TextLine(line_num=14,char_num_start=1, text="100")
    ]
    for e, m in zip(expect, math_lines):
        assert(e.line_num == m.line_num)
        assert(e.text == m.text)


def test_environment_outer():
    env_lines = list(t.iter_environment("chorus"))
    expect = [[
        TextLine(line_num=12, char_num_start=1, text=r"\begin{center}"),
        TextLine(line_num=13, char_num_start=1, text=r"    It's gonna take a lot to take me away from you"),
        TextLine(line_num=14, char_num_start=1, text=r"    There's nothing that a $100$ men or more could ever do"),
        TextLine(line_num=15, char_num_start=1, text=r"    I bless the rains down in Africa"),
        TextLine(line_num=16, char_num_start=1, text=r"    Gonna take some time to do the things we never had"),
        TextLine(line_num=17, char_num_start=1, text=r"    \caption{Bah bah}\label{chorus1}"),
        TextLine(line_num=18, char_num_start=1, text=r"\end{center}"),
    ]]
    for e, m in zip(expect[0], env_lines[0]):
        assert(e.line_num == m.line_num)
        assert(e.text == m.text)


def test_environment_inner():
    env_lines = list(t.iter_environment("center"))
    expect = [[
        TextLine(line_num=13, char_num_start=1, text=r"    It's gonna take a lot to take me away from you"),
        TextLine(line_num=14, char_num_start=1, text=r"    There's nothing that a $100$ men or more could ever do"),
        TextLine(line_num=15, char_num_start=1, text=r"    I bless the rains down in Africa"),
        TextLine(line_num=16, char_num_start=1, text=r"    Gonna take some time to do the things we never had"),
        TextLine(line_num=17, char_num_start=1, text=r"    \caption{Bah bah}\label{chorus1}"),
    ]]
    for e, m in zip(expect[0], env_lines[0]):
        assert(e.line_num == m.line_num)
        assert(e.text == m.text)


def test_command():
    cmd_lines = t.iter_command("section")
    expect = [[
        TextLine(line_num=1, char_num_start=1, text=r"Corrections for $\PT > 50 \GeV$"),
    ]]
    for e, m in zip(expect, cmd_lines):
        for ee, mm in zip(e, m):
            assert(ee.line_num == mm.line_num)
            assert(ee.text == mm.text)

    cmd_lines = t.iter_command("drums")
    expect = [
        [TextLine(line_num=10, char_num_start=1, text=r"yes")],
        [TextLine(line_num=10, char_num_start=1, text=r"big")],
    ]
    for e, m in zip(expect, cmd_lines):
        for ee, mm in zip(e, m):
            assert(ee.line_num == mm.line_num)
            assert(ee.text == mm.text)
