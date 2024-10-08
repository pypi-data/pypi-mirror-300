import sys
import argparse
import docs_maker_messages as dm

from docs_maker.database.init_db_sqlite3 import InitDbSqlite3
from docs_maker.database.init_db_postgres import InitDbPostgres
from docs_maker.cli.version import get_version

l = dm.set_language('ru')

def cli():
    postgres_cmd = 'postgres'
    sqlite3_cmd = 'sqlite3'
    gui_cmd = 'gui'

    parser = argparse.ArgumentParser(prog='docs-maker', description=l.gettext('App Title'))
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {l.gettext("Version")} {get_version("docs_maker")}')
    
    subparser = parser.add_subparsers(dest='commands', help=l.gettext('Commands'))

    pg_parser = subparser.add_parser(postgres_cmd, help=l.gettext('W DB PostgreSQL'))
    pg_parser.add_argument('-d', '--db-name', type=str, help=l.gettext('DB name'))
    pg_parser.add_argument('-U', '--db-username', type=str, help=l.gettext('DB user name'))
    pg_parser.add_argument('-P', '--db-password', type=str, help=l.gettext('DB user password'))
    pg_parser.add_argument('-H', '--hostname', type=str, default='localhost', help=l.gettext('DB hostname'))
    pg_parser.add_argument('-p', '--port', type=str, default='5432', help=l.gettext('DB port'))
        
    sqlite3_parser = subparser.add_parser(sqlite3_cmd, help=l.gettext('W DB SQLite3'))
    sqlite3_parser.add_argument('-d', '--db-name', type=str, help=l.gettext('DB name'))

    gui_parser = subparser.add_parser(gui_cmd, help=l.gettext('GUI parser'))

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    if args.commands == postgres_cmd:
        r_args, _ = pg_parser.parse_known_args()
        if not r_args.db_name and not r_args.db_username and not r_args.db_password:
            pg_parser.print_help()
            sys.exit()
        
        idb = InitDbPostgres(r_args.db_username, r_args.db_password, r_args.hostname, r_args.port, r_args.db_name)
        idb.init()
    
    elif args.commands == sqlite3_cmd:
        r_args, _ = sqlite3_parser.parse_known_args()
        if not any(vars(r_args).values()):
            sqlite3_parser.print_help()
            sys.exit()
            
        idb = InitDbSqlite3(args.db_name)
        idb.init()

    elif args.commands == gui_cmd:
        import docs_maker_gui
        docs_maker_gui.docsMakerRun()
