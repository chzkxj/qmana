
import sys,django,os

#导入项目配置
DjangoObjectPath = '/home/your_objects_path'#修改项目文件夹路径
sys.path.append(DjangoObjectPath) # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'yourobjects.settings' # 修改配置名称
django.setup()

from django.core.mail import send_mail
sender = 'yourname@icloud.com'
receivers = [input('请输入收信人：')]
subject=input('请输入邮件主题：')
content=input('请输入邮件主内容:')

send_mail(
                    subject,
                    content,
                    sender,
                    receivers,
                    fail_silently=False,
                )
