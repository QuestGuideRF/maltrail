from __future__ import print_function
import sys
sys .dont_write_bytecode =True
import optparse
import os
import platform
import threading
import time
import traceback
from core .common import check_connection
from core .common import check_sudo
from core .common import get_ex_message
from core .common import patch_parser
from core .httpd import start_httpd
from core .log import create_log_directory
from core .log import log_error
from core .log import start_logd
from core .settings import config
from core .settings import read_config
from core .settings import CHECK_CONNECTION_MAX_RETRIES
from core .settings import CONFIG_FILE
from core .settings import HOMEPAGE
from core .settings import IS_WIN
from core .settings import NAME
from core .settings import VERSION
from core .update import update_ipcat
from core .update import update_trails
from thirdparty import six
def main ():
    print ("%s (сервер) #v%s {%s}\n"%(NAME ,VERSION ,HOMEPAGE ))
    if "--version"in sys .argv :
        raise SystemExit
    parser =optparse .OptionParser (version =VERSION )
    parser .add_option ("-c",dest ="config_file",default =CONFIG_FILE ,help ="файл конфигурации (по умолчанию: '%s')"%os .path .split (CONFIG_FILE )[-1 ])
    parser .add_option ("--debug",dest ="debug",action ="store_true",help =optparse .SUPPRESS_HELP )
    patch_parser (parser )
    options ,_ =parser .parse_args ()
    print ("[*] начиная с @ %s\n"%time .strftime ("%X /%Y-%m-%d/"))
    read_config (options .config_file )
    if options .debug :
        config .SHOW_DEBUG =True
    if six .PY2 and config .USE_SSL :
        try :
            __import__ ("OpenSSL")
        except ImportError :
            if IS_WIN :
                sys .exit ("[!] пожалуйста, установите «pyopenssl» (например, «pip install pyopenssl»)")
            else :
                msg ="[!] пожалуйста, установите 'pyopenssl'"
                for distros ,install in {("fedora","centos"):"sudo yum установить pyOpenSSL",("debian","ubuntu"):"sudo apt-get установить python-openssl"}.items ():
                    for distro in distros :
                        if distro in (platform .uname ()[3 ]or "").lower ():
                            msg +=" (например, '%s')"%install
                            break
                sys .exit (msg )
        if not config .SSL_PEM or not os .path .isfile (config .SSL_PEM ):
            hint ="openssl req -new -x509 -keyout %s -out %s -days 365 -nodes -subj '/O=%s CA/C=EU'"%(config .SSL_PEM or "server.pem",config .SSL_PEM or "server.pem",NAME )
            sys .exit ("[!] неверное значение конфигурации для 'SSL_PEM' ('%s')\n[?] (подсказка: \"%s\")"%(config .SSL_PEM ,hint ))
    def update_timer ():
        retries =0
        while retries <CHECK_CONNECTION_MAX_RETRIES and not check_connection ():
            sys .stdout .write ("[!] не могу обновиться из-за отсутствия подключения к Интернету (жду..."if not retries else '.')
            sys .stdout .flush ()
            time .sleep (10 )
            retries +=1
        if retries :
            print (")")
        if retries ==CHECK_CONNECTION_MAX_RETRIES :
            print ("[x] собираюсь продолжить без онлайн-обновления")
            _ =update_trails (offline =True )
        else :
            _ =update_trails ()
            update_ipcat ()
        thread =threading .Timer (config .UPDATE_PERIOD ,update_timer )
        thread .daemon =True
        thread .start ()
    if config .UDP_ADDRESS and config .UDP_PORT :
        if config .UDP_PORT <=1024 and not config .DISABLE_CHECK_SUDO and check_sudo ()is False :
            sys .exit ("[!] пожалуйста, запустите «%s» с правами root при использовании значения конфигурации «UDP_ADDRESS»."%__file__ )
        create_log_directory ()
        start_logd (address =config .UDP_ADDRESS ,port =config .UDP_PORT ,join =False )
    try :
        if config .USE_SERVER_UPDATE_TRAILS :
            update_timer ()
        start_httpd (address =config .HTTP_ADDRESS ,port =config .HTTP_PORT ,pem =config .SSL_PEM if config .USE_SSL else None ,join =True )
    except KeyboardInterrupt :
        print ("\r[x] остановка (нажатие Ctrl-C)")
if __name__ =="__main__":
    code =0
    try :
        main ()
    except SystemExit as ex :
        if isinstance (get_ex_message (ex ),six .string_types )and get_ex_message (ex ).strip ('0'):
            print (get_ex_message (ex ))
            code =1
    except IOError :
        log_error ("\n\n[!] session abruptly terminated\n[?] (hint: \"https://stackoverflow.com/a/20997655\")")
        code =1
    except Exception :
        msg ="\r[!] Произошло необработанное исключение ('%s')"%sys .exc_info ()[1 ]
        msg +="\n[x] please report the following details at 'https://github.com/stamparm/maltrail/issues':\n---\n'%s'\n---"%traceback .format_exc ()
        log_error ("\n\n%s"%msg .replace ("\r",""))
        print (msg )
        code =1
    finally :
        if not any (_ in sys .argv for _ in ("--version","-h","--help")):
            print ("\n[*] заканчивается @ %s"%time .strftime ("%X /%Y-%m-%d/"))
        os ._exit (code )