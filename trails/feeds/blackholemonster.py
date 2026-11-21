from core .common import retrieve_content
__url__ ="https://blackhole.monster/blackhole-today"
__check__ =".1"
__info__ ="известный злоумышленник"
__reference__ ="ip.blackhole.monster"
def fetch ():
    retval ={}
    content =retrieve_content (__url__ )
    if __check__ in content :
        for line in content .split ('\n'):
            line =line .strip ()
            if not line or line .startswith ('#')or '.'not in line :
                continue
            retval [line ]=(__info__ ,__reference__ )
    return retval