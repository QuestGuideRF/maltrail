from core .common import retrieve_content
__url__ ="https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.txt"
__check__ ="Feodo"
__info__ ="смайл (вредоносное ПО)"
__reference__ ="abuse.ch"
def fetch ():
    retval ={}
    content =retrieve_content (__url__ )
    if __check__ in content :
        for line in content .split ('\n'):
            line =line .strip ()
            if not line or line .startswith ('#'):
                continue
            retval [line ]=(__info__ ,__reference__ )
    return retval