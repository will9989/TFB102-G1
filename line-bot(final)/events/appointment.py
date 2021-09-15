# appointment_step1選擇服務 => 此步驟完成
# appointment_step1選擇時間
# appointment_step1完成預約
from line_bot_api import *


def appointment_step1(event):
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(

                    title='請選擇推薦項目',
                    text='Please select service',
                    actions=[
                        PostbackAction(
                            label='餐廳',
                            display_text='餐廳',
                            data='餐廳'

                        ),
                        PostbackAction(
                            label='文章',
                            display_text='文章',
                            data='文章'
                        )

                    ]
                )
            ]
        )
    )

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=[
                  carousel_template_message]
    )

