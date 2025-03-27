# -*- coding: utf-8 -*-
import os
import random
import time

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage
from plugins import (
    weather_api,
    img_upload,
    fortune_by_sqlite,
    user_todo_list,
    main,
    githubUpload,
)

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    # 判断数据库初是否始化
    fortune_by_sqlite.database_initialized()

    async def on_group_at_message_create(self, message: GroupMessage):
        msg = message.content.strip()
        member_openid = message.author.member_openid
        print("[Info] bot 收到消息：" + message.content)

        if msg == f"我喜欢你":
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"我也喜欢你",
            )

        elif msg.startswith("/漫画"):
            mangaId = msg.replace("/漫画", "").strip()
            msgseq = int(time.time() * 1000) + random.randint(0, 999)
            message.reply(content=f"文件上传ing", msgseq=msgseq)
            # flag = 0
            # file_url = ""
            # # TODO: 只能上传单个id
            # a = main.autoDown(mangaId)
            # # TODO: 重复文件上传有问题
            # if a is not None:
            #     flag = githubUpload.upload(
            #         f"D:/pythonProject/JMComic/18comic_dow/books/{a}.zip"
            #     )
            # else:
            #     await message._api.post_group_message(
            #         group_openid=message.group_openid,
            #         msg_type=0,
            #         msg_id=message.id,
            #         content=f"内存溢出或文件上传失败，尝试查看图床确认",
            #     )
            #     return
            # if flag is not 0:
            #     # file_url = githubUpload.getImage(f"{a}.zip")
            #     # file_url = githubUpload.getImage(f"00003.jpg")
            #     # 上传完毕
            #     messageResult = await message._api.post_group_message(
            #         group_openid=message.group_openid,
            #         msg_type=0,
            #         msg_id=message.id,
            #         content=f"您的本子已打包，前往https://git😀hub😀.com/Afwct/image/tree/main/JMComic查看吧",
            #     )
            # else:
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"文件上传失败",
            )
            return
            # if file_url is None:
            #     await message._api.post_group_message(
            #         group_openid=message.group_openid,
            #         msg_type=0,
            #         msg_id=message.id,
            #         content=f"文件获取失败",
            #     )
            #     return
            # print(file_url)
            # # 机器人文件回传 TODO: 超时
            # messageResult = await message._api.post_group_file(
            #     group_openid=message.group_openid,
            #     file_type=1,
            #     url=file_url,
            # )
            # # 资源上传后，会得到Media，用于发送消息
            # await message._api.post_group_message(
            #     group_openid=message.group_openid,
            #     msg_type=7,
            #     msg_id=message.id,
            #     media=messageResult,
            #     content=f"您的本子喵",
            # )

        elif msg.startswith("/今日运势"):

            result = fortune_by_sqlite.get_today_fortune(member_openid)
            file_url = img_upload.get_upload_history()
            # print(result)
            messageResult = await message._api.post_group_file(
                group_openid=message.group_openid, file_type=1, url=file_url
            )
            # 资源上传后，会得到Media，用于发送消息
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                media=messageResult,
                content=f"{result}",
            )

        elif msg.startswith("/test"):
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"\nBoost & Magnum, ready fight!!!",
            )

        elif msg.startswith("/天气"):
            city_name = msg.replace("/天气", "").strip()
            result = weather_api.format_weather(city_name)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}",
            )

        elif msg.startswith("/查询"):
            file_url = img_upload.upload(
                "../examples/imgs/img_test.jpg"
            )  # 此处填写你要上传图片的地址
            # file_url = f"https://s21.ax1x.com/2024/12/08/pA7DmAP.jpg"  # 这里需要填写上传的资源Url

            messageResult = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,  # 文件类型要对应上，具体支持的类型见方法说明
                url=file_url,  # 文件Url
            )

            # 资源上传后，会得到Media，用于发送消息
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=messageResult,
            )
            img_upload.delete_img()  # 从图床中删除图片，防止重复上传

        elif msg.startswith("/待办"):
            msgs = msg.replace("/待办", "").strip()
            author = message.author.__dict__

            msg_user = author["member_openid"]
            print("[Info] message author is: " + msg_user)
            if msgs.startswith("-s"):
                todo_list = user_todo_list.show(msg_user)
                if todo_list == -1:
                    content1 = "没有查询到该用户的待办呢。\n已为您创建用户。"
                else:
                    content1 = "\n待办有如下哦：\n"
                    for todo in todo_list:
                        todo = "\n" + todo + "\n"
                        content1 = content1 + todo

                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=content1,
                )

            elif msgs.startswith("-d"):
                msg_all = msgs.replace("-d", "").strip()
                msg_num = msg_all
                flag = user_todo_list.delete(msg_user, int(msg_num))
                if flag == 1:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"成功删除第{msg_num}条待办",
                    )
                elif flag == -2:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"不存在这条待办哦",
                    )
                else:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="没有查询到该用户的待办呢。\n已为您创建用户。",
                    )
            elif msgs.startswith("-i"):
                msg_todo = msgs.replace("-i", "").strip()
                flag = user_todo_list.insert(msg_user, msg_todo)
                if flag == 1:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"成功添加待办，今后也要加油哦(ง •_•)ง",
                    )
                else:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="没有查询到该用户的待办呢。\n已为您创建用户。",
                    )
            elif msgs.startswith("-clear"):
                flag = user_todo_list.init(msg_user)
                if flag == 1:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="已为您成功清除所有待办！",
                    )
                else:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="没有查询到该用户的待办呢。\n已为您创建用户。",
                    )

            else:
                content2 = "\n\n'/待办' 的用法：\n  '-s'显示您所有待办\n  '-d 序号' 删除第几条待办 \n  '-i' 添加待办\n  '-clear' 清除所有待办"
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=content2,
                )

        else:
            print("Normal")
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"收到：{msg}",
            )

        _log.info(messageResult)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
