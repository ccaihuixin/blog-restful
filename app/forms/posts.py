from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length

class PostsForm(FlaskForm):
    # 设置字段的其他属性使用render_kw完成
    title = StringField('', validators=[DataRequired(), Length(5, 100, message='标题长度请介于5至100之间')],
                        render_kw={"placeholder": '文章的标题'})
    content = TextAreaField(render_kw={'placeholder': '请输入文章内容', 'rows': '24', 'style': 'resize:none'},
                            validators=[DataRequired(), Length(1, 65535, message="长度要介于1，128之间")])
    submit = SubmitField('发表')


class ChangePostsForm(FlaskForm):
    # 设置字段的其他属性使用render_kw完成
    id = IntegerField("", render_kw={"style": "display:none"})
    title = StringField('', validators=[DataRequired(), Length(5, 100, message='标题长度请介于5至100之间')],
                        render_kw={"placeholder": '文章的标题'})
    content = TextAreaField(render_kw={'placeholder': '请输入文章内容', 'rows': '24', 'style': 'resize:none'},
                            validators=[DataRequired(), Length(1, 65535, message="长度要介于1，128之间")])
    submit = SubmitField('发表')

