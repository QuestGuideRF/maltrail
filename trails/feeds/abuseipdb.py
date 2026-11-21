from core .common import retrieve_content
__url__ ="https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/main/abuseipdb-s100-1d.ipv4"
__check__ =".1"
__info__ ="известный злоумышленник"
__reference__ ="abuseipdb.com"
def fetch ():
    retval ={}
    content =retrieve_content (__url__ )
    if __check__ in content :
        for line in content .split ('\n'):
            line =line .split ('#')[0 ].strip ()
            if not line or line .startswith ('#')or '.'not in line :
                continue
            retval [line ]=(__info__ ,__reference__ )
    return retval