import json

class ServerSelecter():
    def __init__(self):
        pass

    def createCarousel(self, server_list):
        bubble_list = []
        for server in server_list:
            bubble_list.append(self.createBubble(server.get('name'), server.get('local_ip')))

        carousel = {
            "type": "carousel",
            "contents": bubble_list
        }

        return carousel
    

    def createBubble(self, server_name, local_ip):
        bubble = {
            "type": "bubble",
            "size": "micro",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": server_name,
                        "color": "#ffffff",
                        "align": "start",
                        "size": "md",
                        "gravity": "center"
                    }
                ],
                "backgroundColor": "#27ACB2",
                "paddingTop": "19px",
                "paddingAll": "12px",
                "paddingBottom": "16px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "color": "#8C8C8C",
                                "size": "sm",
                                "wrap": True,
                                "text": local_ip
                            }
                        ],
                        "flex": 1
                    }
                ],
                "spacing": "md",
                "paddingAll": "12px"
            },
            "action": {
                "type": "postback",
                "label": "action",
                "data": local_ip,
                "displayText": f"Connect to {server_name}"
            },
            "styles": {
                "footer": {
                    "separator": False
                }
            }
        }

        return bubble