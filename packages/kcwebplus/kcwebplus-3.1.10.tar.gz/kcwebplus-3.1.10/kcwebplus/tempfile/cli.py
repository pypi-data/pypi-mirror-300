# 该文件可通过python 运行  如：python cli.py
import kcweb,app,sys
app=kcweb.web(__name__,app)
if __name__ == "__main__":
    try:
        route=sys.argv[1]
    except:
        print('命令格式错误 请参考以下命令')
        print('格式：python cli.py 路由地址')
        print('示例：python cli.py index/index')
    else:
        app.cli(route)
    # app.cli('index/index')