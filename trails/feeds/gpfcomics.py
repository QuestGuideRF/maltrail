from core .common import retrieve_content
__url__ ="https://iplists.firehol.org/files/gpf_comics.ipset"
__check__ ="comics"
__info__ ="известный злоумышленник"
__reference__ ="gpf-comics.com"
def fetch ():
    retval ={}
    content =retrieve_content (__url__ )
    for line in content .split ('\n'):
        line =line .strip ()
        if not line or line .startswith ('#')or '.'not in line :
            continue
        retval [line ]=(__info__ ,__reference__ )
    return retval