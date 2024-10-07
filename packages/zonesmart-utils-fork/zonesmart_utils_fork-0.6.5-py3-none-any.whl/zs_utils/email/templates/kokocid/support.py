from zs_utils.email.templates.kokocid import base

subject_ru = "Обращение из Kokoc ID"

title_ru = "Kokoc ID: Обращение в поддержку"

body_ru = """
    <tr>
        <td style="padding-right: 32px; padding-left: 32px; border-radius: 12px; margin-bottom: 16px;">
            <table align="left" border="0" cellspacing="0" cellpadding="0" role="presentation">
                <tr>
                    <td>
                        <h2 style="
                        margin: 0;
                        font-weight: 400;
                        font-size: 16px;
                        line-height: 150%;
                        color: #757070;">
                          Email пользователя: {email}
                        </h2>
                        <h2 style="
                        margin: 0;
                        font-weight: 400;
                        font-size: 16px;
                        line-height: 150%;
                        color: #757070;">
                          Телефон пользователя: {phone}
                        </h2>
                        <h2 style="
                        margin: 0;
                        margin-bottom: 24px;
                        font-weight: 400;
                        font-size: 16px;
                        line-height: 150%;
                        color: #757070;">
                          Страница обращения: {page}
                        </h2>
                    </td>
                </tr>
                <tr>
                    <td>
                        <p style="
                        font-weight: 400;
                        font-size: 16px;
                        line-height: 150%;
                        color: #757070;
                        margin-top: 0;
                        margin-bottom: 12px;"
                        >
                          Обращение:<br>
                          {body}
                        </p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
"""