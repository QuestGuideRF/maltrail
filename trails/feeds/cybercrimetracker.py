import re
from core .common import fetch_headers
from core .common import retrieve_content
__url__ ="https://cybercrime-tracker.net/all.php"
__check__ ="cp.php?m=логин"
__info__ ="malware"
__reference__ ="cybercrime-tracker.net"
def fetch ():
    retval ={}
    headers =fetch_headers (__url__ )
    location =headers .get ("Location","")
    match =re .search (r"\?(__r=[\w.]+)",location )
    if match :
        content =retrieve_content (__url__ ,headers ={"Cookie":match .group (1 )})
        if __check__ in content :
            content =content .replace ("<br />",'\n')
            for line in content .split ('\n'):
                line =line .strip ()
                if not line or line .startswith ('#')or '(SSL)'in line :
                    continue
                if '://'in line :
                    line =re .search (r"://(.*)",line ).group (1 )
                line =line .rstrip ('/')
                if '/'in line :
                    retval [line ]=(__info__ ,__reference__ )
                    line =line .split ('/')[0 ]
                if ':'in line :
                    line =line .split (':')[0 ]
                if re .search (r"\A\d+\.\d+\.\d+\.\d+\Z",line ):
                    retval [line ]=("сайт потенциального вредоносного ПО",__reference__ )
                else :
                    retval [line ]=(__info__ ,__reference__ )
    return retval