import i18n
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')

if localedir not in i18n.load_path:
    i18n.load_path.append(localedir)


# import os
# import configparser
# def read_ini_value():
#     try:
#         # 获取用户个人目录
#         user_profile = os.getenv('USERPROFILE') or os.getenv('HOME')
#         if user_profile is None:
#             raise EnvironmentError("环境变量 USERPROFILE 或 HOME 未设置")
        
#         # 构造完整路径（Windows路径和Linux/macOS路径不同）
#         if os.name == 'nt':  # Windows
#             file_path = os.path.join(user_profile, 'AppData', 'Roaming', 'biolab.si', 'language.ini')
#         else:  # macOS 和 Linux
#             file_path = os.path.join(user_profile, '.config', 'biolab.si', 'BlueWhale.ini')

#         # 检查文件是否存在
#         if not os.path.isfile(file_path):
#             raise FileNotFoundError(f"文件未找到: {file_path}")

#         # 创建一个ConfigParser对象
#         config = configparser.ConfigParser()
#         config.read(file_path)

#         # 获取并打印指定键的值
#         value = config.get('application-style', 'languages')
#         return value

#     except (EnvironmentError, FileNotFoundError) as e:
#         print(f"路径错误: {e}")
#     except (configparser.NoSectionError, configparser.NoOptionError) as e:
#         print(f"配置文件错误: {e}")
#     except Exception as e:
#         print(f"读取文件时发生错误: {e}")

#     # 返回默认值
#     return 'en'


# # 主程序调用
# default_value = read_ini_value()
# i18n.set('locale', default_value)



