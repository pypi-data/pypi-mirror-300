import argparse


def main():
    parser = argparse.ArgumentParser(prog="dgtest", description="大刚测试开发实战项目")
    # 不加 - 的前缀 表示必填参数，加 - 表示可选参数，- 为缩写 -- 为全称
    parser.add_argument("-n", "--name", default="大刚", help="测试开发实战的作者姓名")
    parser.add_argument("-a", "--age", default="18", help="测试开发实战的作者年龄")
    args = parser.parse_args()
    if args.name:
        print(f"Welcome to '{args.name}测试开发实战', author by {args.name}")
        print(f"The author age is {args.age}")


if __name__ == '__main__':
    main()