from core .common import retrieve_content
__url__ ="http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
__check__ ="Последний отчет"
__info__ ="известный злоумышленник"
__reference__ ="rulez.sk"
def fetch ():
    retval ={}
    content =retrieve_content (__url__ )
    if __check__ in content :
        for line in content .split ('\n'):
            line =line .strip ()
            if not line or line .startswith ('#')or '.'not in line :
                continue
            retval [line .split ('\t')[0 ]]=(__info__ ,__reference__ )
    return retval