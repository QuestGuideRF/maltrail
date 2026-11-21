from core .common import retrieve_content
__url__ ="https://raw.githubusercontent.com/scriptzteam/badIPS/main/ips.txt"
__check__ =".1"
__info__ ="плохая репутация"
__reference__ ="github.com/scriptzteam/badIPS"
def fetch ():
    retval ={}
    content =retrieve_content (__url__ )
    if __check__ in content :
        for line in content .split ('\n'):
            line =line .strip ()
            if not line or line .startswith ('#')or line .count ('.')!=3 :
                continue
            retval [line ]=(__info__ ,__reference__ )
    return retval