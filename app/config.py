import os

base_dir = os.path.abspath(os.path.dirname(__name__))

# 通用配置
class Config:
    # 密钥
    # 不用中文
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    # 数据库操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.qq.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '1250653250@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'qhimqpfkngwrbafg'
    # 使用本地库中的bootstrap依赖包
    BOOTSTRAP_SERVER_LOCAL = True

    # 文件上传
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'app/static/upload')

    # 初始化方法
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/blog"


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/blog"


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/blog"


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
