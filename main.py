from src.executor import Executor


if __name__ == "__main__":
    argparser = Executor.create_arg_parser()
    args = argparser.parse_args()
    with Executor(**vars(args)) as executor:
        executor.run()