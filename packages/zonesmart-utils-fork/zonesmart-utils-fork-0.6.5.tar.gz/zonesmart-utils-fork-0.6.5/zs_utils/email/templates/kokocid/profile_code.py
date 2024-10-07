from zs_utils.email.templates.kokocid import base

subject_ru = "Смена почты Kokoc ID"

title_ru = "Kokoc ID: Смена почты"

body_ru = """
    <tr>
        <td>
            <h2 style="
            margin: 0;
            margin-bottom: 24px;
            font-weight: 400;
            font-size: 16px;
            line-height: 150%;
            color: #757070;">Здравствуйте, Вы получили это сообщение, так как ваш адрес был указан при смене почты в сервисе Kokoc ID.</h2>
        </td>
    </tr>
    <tr>
        <td>
            <p style="
            margin-top: 0;
            margin-bottom: 8px;
            font-weight: 700;
            font-size: 16px;
            line-height: 150%;
            color: #403839;">
                Ваш код подтверждения: </p>
        </td>
    </tr>
    <tr>
        <td>
            <p style="border-bottom: 2px solid #e1e1e1;
            margin-top: 0;
            margin-bottom: 24px;
            background: #f7f7f7;
            font-weight: 700;
            font-size: 24px;
            line-height: 150%;
            color: #f6664b;
                padding: 20px 28px;">
                {code}
            </p>
        </td>
    </tr>
"""