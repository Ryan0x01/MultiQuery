class Options:
    def __init__(self, parser):
        # 初始化
        args = parser.parse_args()
        if not any(vars(args).values()):
            parser.parse_args(["-h"])
        # 参数赋值
        self.query = args.q
        self.type = args.t
        self.file = args.f
        self.out_file = ''
        if args.l:
            self.limit = args.l
        else:
            self.limit = 0
        if args.db:
            self.out = "db"
        elif args.o:
            self.out = "excel"
            self.out_file = args.o
        else:
            self.out = "print"
