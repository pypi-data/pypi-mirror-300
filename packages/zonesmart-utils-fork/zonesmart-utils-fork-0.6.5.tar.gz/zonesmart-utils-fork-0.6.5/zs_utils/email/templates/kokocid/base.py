logo = "kokocid.png"

base_template = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email-рассылка</title>
</head>
<body style="background-color: #eee;">
    <table align="center" border="0" cellspacing="0" cellpadding="0" role="presentation" style="padding-top: 132px; padding-bottom: 132px;font-family: Arial, Helvetica, sans-serif; font-style: normal; font-weight: 400; font-size: 16px; line-height: 130%;">
        <tr>
            <td>
                <table align="center" border="0" cellspacing="0" cellpadding="0" role="presentation" style="max-width: 600px; width: 100%; background-color: #fff;">
                    <tr style="display: block; background: #fafafa; padding: 29px 32px;">
                        <td>
                            <img src="{logo_url}" alt="">
                        </td>
                    </tr>
                    <tr style="padding-right: 32px;padding-left: 32px;padding-top: 32px; display: block;">
                        <td>
                            <h1 style="font-weight: 700;
                            font-size: 20px;
                            margin-bottom: 12px;
                            margin-top: 0;
                            line-height: 150%;
                            color: #403839;
                            ">{title}</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-right: 32px; padding-left: 32px; border-radius: 12px; margin-bottom: 16px;">
                            <table align="center" border="0" cellspacing="0" cellpadding="0" role="presentation">
                                {body}
                                <tr>
                                    <td>
                                        <p style="
                                        font-weight: 400;
                                        font-size: 16px;
                                        line-height: 150%;
                                        color: #757070;
                                        margin-top: 0;
                                        margin-bottom: 12px;">
                                            Внимание! <br>
                                            Если вы не запрашивали отправку этого письма, просто проигнорируйте его<br>
                                            С уважением, команда Kokoc ID

                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <h3 style="
                                        margin-top: 0;
                                        margin-bottom: 32px;
                                            font-weight: 400;
                                            font-size: 16px;
                                            line-height: 150%;
                                            color: #aba8a8;
                                        ">Сообщение сгенерировано автоматически.</h3>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr style="background: #f2f2f2; display: block; display: flex; justify-content: space-between; padding: 35px 32px;
                    font-size: 12px;
                    font-style: normal;
                    font-weight: 400;
                    line-height: 130%; /* 15.6px */
                    letter-spacing: -0.12px;">
                    <td >
                        <a href="/"
                            style="
                            max-width: 130px;
                            font-weight: 400;
                            margin: 0;
                            margin-right: 16px;
                            font-size: 12px;
                            line-height: 150%;
                            text-decoration: underline;
                            text-decoration-skip-ink: none;
                            color: #aba8a8;">
                                Помощь и поддержка
                        </a>

                    </a>
                    </td>
                    <td>
                        <a href="/" style="
                        font-weight: 400;
                        margin: 0;
                        margin-right: 40px;
                        font-size: 12px;
                        line-height: 150%;
                        text-decoration: underline;
                        text-decoration-skip-ink: none;
                        color: #aba8a8;">
                            Политика обработки персональных данных
                    </a>
                    </td>
                    <td>
                        <p style="
                        margin: 0;
                        font-weight: 400;
                        font-size: 12px;
                        line-height: 139%;
                        color: #aba8a8;">2024, © Kokoc Group</p>
                    </td>
                </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
