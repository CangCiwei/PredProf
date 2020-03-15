import cmd
import storage

week = {'Пн': 1 , 'Вт': 2, 'Ср': 3, 'Чт': 4, 'Пт': 5, 'Сб': 6, 'Вс': 7}

error_message = 'Ошибка' 

class Cli(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "Здравствуйте, для ознакомления с функционалом: help" 
        self.doc_header = "Доступные команды, для пояснения: help <название_команды>"

    def do_get_schedule(self, args):
        """Вывод расписания:
            1) аргумент = '' - все расписание
            2) аргумент = день недели в формате: 'пн' - конкретный день"""
        if args == '':
            print(storage.get_schedule())
        elif args in week:
            print(storage.get_schedule(week[args]))
        else:
            print("Ошибка ввода")

    def do_change_schedule(self, args):
        """Изменение расписания, формат: <День недели>, <Урок 1>, <Урок 2> и т.д."""
        args = args.split()
        if args[0] in week.keys():
            day = week[args[0]]
            storage.change_schedule(day, args[1:])
        else:
            print("Ошибка ввода")

    def do_add_note(self, args):
        """Добавление заметки, формат: <day> <event> <note>"""
        args = args.split()
        if len(args) > 2 and args[0] in week.keys():
            day = week[args[0]]
            event = args[1]
            note = args[2:]
            storage.add_note(day, event, note)
        else:
            print("Ошибка ввода")

    def do_add_todo(self, args):
        """Добавление домашнего задания, формат: <День> <Предмет> <Д/З> is_done"""
        args = args.split()
        if len(args) > 2 and args[0] in week.keys():
            day = week[args[0]]
            event = args[1]
            note = args[2:]
            storage.add_note(day, event, note, todo=True)
        else:
            print("Ошибка ввода")

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
        args = args.split()
        if len(args) == 3 and args[0] in week.keys():
            day = week[args[0]]
            event = args[1]
            note_num = args[2]
            storage.get_note(day, event, int(note_num))
        else:
            print("Ошибка ввода")
    
    def do_get_all_todo(self, a):
        for idd, note in enumerate(storage.get_all_notes()):
            print(n)
        

    def do_exit(self, strr):
        """Выход"""
        exit()

    def default(self, line):
        print("Ошибка ввода")

if __name__ == "__main__":
    cli = Cli()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        exit()
