import websocket
import rel
import requests
import json
sortWord = [
    ["x","彳亍"],
    ["nya","喵 !"],
    ["th","🤔"],
    ["t","听我说谢谢你~"],
    ["🌚","m"],
    ["😝","h"]
]
def sendPrivateMessage(id, message):
    requests.get("http://127.0.0.1:5702/send_msg?user_id=%d&message=%s" % (id, message))
def sendGroupMessage(id, message):
    requests.get("http://127.0.0.1:5702/send_group_msg?group_id=%d&message=%s" % (id, message))
def delMessage(id):
    requests.get("http://127.0.0.1:5702/delete_msg?message_id=%d" % (id))
def getMessage(ws, message):
    m = dict(json.loads(message))
    if m["post_type"] == "message_sent":
        try:
            if m["message"].split()[0] == ".":
                messageid = m["message_id"]
                for listIndex in range(0,len(sortWord)):
                    if m["message"].split()[1] == sortWord[listIndex][0]:
                        if m["message_type"] == "private":
                            delMessage(messageid)
                            sendPrivateMessage(m["target_id"],sortWord[listIndex][1])
                        if m["message_type"] == "group":
                            delMessage(messageid)
                            sendGroupMessage(m["group_id"],sortWord[listIndex][1])
        except:
            pass
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:5703/", on_message=getMessage)
    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()