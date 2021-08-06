$(function(){
        // 评论提交
    $(".comment_form").submit(function (e) {
            e.preventDefault();
            // 获取当前标签中的,文章编号,评论内容
            var post_id = $(this).attr('data-postid')
            var post_comment = $(".comment_input").val();

            if (!post_comment) {
                alert('请输入评论内容');
                return
            }
            var params = {
                "post_id": post_id,
                "comment": post_comment
            };
            $.ajax({
                url: "/article/article_comment",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify(params),
                success: function (resp) {
                    if (resp.errno == '0') {
                        var comment = resp.data
                        // 拼接内容
                        var comment_html = ''
                        comment_html += '<div class="comment_list">'
                        comment_html += '<div class="person_pic fl">'
                        if (comment.user.icon) {
                            comment_html += '<img src="../../static/upload/' + comment.user.icon+'" alt="用户图标">'
                        }else {
                            comment_html += '<img src="../../static/upload/' + comment.user.icon+'" alt="用户图标">'
                        }
                        comment_html += '</div>'
                        comment_html += '<div class="user_name fl">' + comment.user.username + '</div>'
                        comment_html += '<div class="comment_text fl">'
                        comment_html += comment.content
                        comment_html += '</div>'
                        comment_html += '<div class="comment_time fl">' + comment.create_time + '</div>'

                        comment_html += '<a href="javascript:;" class="comment_up fr" data-commentid="' + comment.id + '" data-postid="' + comment.post_id + '">赞</a>'
                        comment_html += '<a href="javascript:;" class="comment_reply fr">回复</a>'
                        comment_html += '<form class="reply_form fl" data-commentid="' + comment.id + '" data-postid="' + post_id + '">'
                        comment_html += '<textarea class="reply_input"></textarea>'
                        comment_html += '<input type="button" value="回复" class="reply_sub fr">'
                        comment_html += '<input type="reset" name="" value="取消" class="reply_cancel fr">'
                        comment_html += '</form>'

                        comment_html += '</div>'
                        // 拼接到内容的前面
                        $(".comment_list_con").prepend(comment_html)
                        // 让comment_sub 失去焦点
                        $('.comment_sub').blur();
                        // 清空输入框内容
                        $(".comment_input").val("")

                        //更新评论数量
                        updateCommentCount();
                    }else {
                        alert(resp.errmsg)
                    }
                }
            })

    })

    // 给a,input标签添加了代理事件
    $('.comment_list_con').delegate('a,input','click',function(){

        //获取到点击标签的class属性, reply_sub
        var sHandler = $(this).prop('class');

        if(sHandler.indexOf('comment_reply')>=0)
        {
            $(this).next().toggle();
        }

        if(sHandler.indexOf('reply_cancel')>=0)
        {
            $(this).parent().toggle();
        }

        // 点赞处理
        if(sHandler.indexOf('comment_up')>=0)
        {

            var $this = $(this);
            var action = "add"
            if(sHandler.indexOf('has_comment_up')>=0)
            {
                // 如果当前该评论已经是点赞状态，再次点击会进行到此代码块内，代表要取消点赞
                action = "remove"
            }
            //获取到当前点击的标签上面的, 评论编号, 新闻编号
            var comment_id = $(this).attr("data-commentid")
            // var post_id = $(this).attr("data-postid")
            var params = {
                "comment_id": comment_id,
                "action": action,
                // "news_id": news_id
            }

            $.ajax({
                url: "/article/article_like",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify(params),
                success: function (resp) {
                    if (resp.errno == "0") {
                        //获取到当前标签中的点赞数量
                        var like_count = $this.attr('data-likecount')

                        //增加安全性校验,如果获取不到data-likecount的值,那么默认设置成0
                        if(like_count == undefined){
                            like_count = 0;
                        }

                        // 更新点赞按钮图标,并加1, 减1操作
                        if (action == "add") {
                            like_count = parseInt(like_count) + 1
                            // 代表是点赞
                            $this.addClass('has_comment_up')
                        }else {
                            like_count = parseInt(like_count) - 1
                            $this.removeClass('has_comment_up')
                        }

                        // 更新点赞数据,重新赋值回去
                        $this.attr('data-likecount', like_count)
                        if (like_count == 0) {
                            $this.html("赞")
                        }else {
                            $this.html(like_count)
                        }
                    }else if (resp.errno == "4101"){
                        $('.login_form_con').show();
                    }else {
                        alert(resp.errmsg)
                    }
                }
            })

        }

        // 评论回复
        if(sHandler.indexOf('reply_sub')>=0)
        {

            var $this = $(this)
            var post_id = $this.parent().attr('data-postid')
            var parent_id = $this.parent().attr('data-commentid')
            var comment = $this.prev().val()

            if (!comment) {
                alert('请输入评论内容')
                return
            }
            var params = {
                "post_id": post_id,
                "comment": comment,
                "parent_id": parent_id
            }
            $.ajax({
                url: "/article/article_comment",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify(params),
                success: function (resp) {
                    if (resp.errno == "0") {
                        var comment = resp.data
                        // 拼接内容
                        var comment_html = ""
                        comment_html += '<div class="comment_list">'
                        comment_html += '<div class="person_pic fl">'
                        if (comment.user.icon) {
                            comment_html += '<img src="../../static/upload/' + comment.user.icon+'" alt="用户图标">'
                        }else {
                            comment_html += '<img src="../../static/upload/' + comment.user.icon+'" alt="用户图标">'
                        }
                        comment_html += '</div>'
                        comment_html += '<div class="user_name fl">' + comment.user.username + '</div>'
                        comment_html += '<div class="comment_text fl">'
                        comment_html += comment.content
                        comment_html += '</div>'
                        comment_html += '<div class="reply_text_con fl">'
                        comment_html += '<div class="user_name2">' + comment.parent.user.username + '</div>'
                        comment_html += '<div class="reply_text">'
                        comment_html += comment.parent.content
                        comment_html += '</div>'
                        comment_html += '</div>'
                        comment_html += '<div class="comment_time fl">' + comment.create_time + '</div>'

                        comment_html += '<a href="javascript:;" class="comment_up fr" data-commentid="' + comment.id + '" data-postid="' + comment.post_id + '">赞</a>'
                        comment_html += '<a href="javascript:;" class="comment_reply fr">回复</a>'
                        comment_html += '<form class="reply_form fl" data-commentid="' + comment.id + '" data-postid="' + post_id + '">'
                        comment_html += '<textarea class="reply_input"></textarea>'
                        comment_html += '<input type="button" value="回复" class="reply_sub fr">'
                        comment_html += '<input type="reset" name="" value="取消" class="reply_cancel fr">'
                        comment_html += '</form>'

                        comment_html += '</div>'
                        $(".comment_list_con").prepend(comment_html)
                        // 请空输入框
                        $this.prev().val('')
                        // 关闭
                        $this.parent().hide()

                        //更新评论数量
                        updateCommentCount();
                    }else {
                        alert(resp.errmsg)
                    }
                }
            })

        }
    })
})

// 更新评论条数
function updateCommentCount() {
    var length = $(".comment_list").length
    $(".comment_count").html(length + "条评论")
}