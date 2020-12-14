class Terminal():
    def __init__(self):
        pass

    def createTerminalResponse(self, server_name, current_dir, std_out):
        res = {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": server_name,
                        "color": "#ffffff99",
                        "size": "sm"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": current_dir,
                        "color": "#ffffff99",
                        "size": "sm"
                    }
                    ]
                }
                ],
                "paddingAll": "20px",
                "backgroundColor": "#27ACB2",
                "spacing": "md",
                "height": "90px",
                "paddingTop": "22px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": std_out,
                    "wrap": True,
                    "color": "#000000",
                    "size": "xs"
                }
                ]
            }
        }

        return res