import cmd
import storage

days = {'mon': 1 , 'tue': 2, 'etc...': 'etc...'}

error_message = 'er' #сообщение об ошибке, могут быть разными

def prepare_schedule(data):
    """Преобразует набранное дневное расписание в словарь вида {1: 'Матматика', 2: 'Русский язык, '}"""
    pass

class Cli(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "Приветствие" 
        self.doc_header = "Доступные команды 'help _команда_'"

    def do_get_schedule(self, args):
        """Описание"""
        if args == '':
            print(storage.get_schedule())
        elif args in map(str, range(1, 8)):
            print(storage.get_schedule(int(args)))
        else:
            print(error_message)

    def do_change_schedule(self, args):
        """Описание"""
        if len(args.split()) > 1:
            day = args.split()[0]
            if days.get(day):
                schedule = prepare_schedule(args[1:])
                storage.change_schedule(days.get(day), schedule)
            else:
                print(error_message)
        else:
            print(error_message)

    def do_add_note(self, args):
        """Описание"""
        if len(args.split()) > 2:
            day = args.split()[0]
            event = args.split()[1]
            note = args.split()[2:]
            if days.get(day) and event.isdigit():
                storage.add_note(days.get(day), int(event), note)
            else:
                print(error_message)
        else:
            print(error_message)

    def do_add_todo(self, args):
        """Описание"""
        if len(args.split()) > 2:
            day = args.split()[0]
            event = args.split()[1]
            note = args.split()[2:]
            if days.get(day) and event.isdigit():
                storage.add_note(days.get(day), int(event), note, todo=True)
            else:
                print(error_message)
        else:
            print(error_message)

    def do_mark_as_done(self, args):
        if len(args.split()) == 3:
            day = args.split()[0]
            event = args.split()[1]
            note_num = args.split()[2]
            if days.get(day) and event.isdigit() and note_num.isdigit():
                storage.done(days.get(day), int(event), int(note_num))
            else:
                print(error_message)
        else:
            print(error_message)

    def do_get_note(self, args):
        if len(args.split()) == 3:
            day = args.split()[0]
            event = args.split()[1]
            note_num = args.split()[2]
            if days.get(day) and event.isdigit() and note_num.isdigit():
                storage.get_note(days.get(day), int(event), int(note_num))
            else:
                print(error_message)
        else:
            print(error_message)

    def do_exit(self, args):
        """Описание"""
        exit()

    def do_q(self, args):
        """Описание"""
        exit()

    def default(self, line):
        print(error_message)

if __name__ == "__main__":
    cli = Cli()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        exit()
