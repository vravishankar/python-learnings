import json
Buttons = []
Buttons.append({"title":"Incidents","payload":"/inform{\"search_type\":\"incidents\""})
Buttons.append({"title":"Changes","payload":"/inform{"search_type":"changes""})
# Buttons.append({"title":"High","payload":"high"})
# Buttons.append({"title":"Medium","payload":"medium"})

payload = {}
payload['channel_id']='sdfsdfsdfsdfsdfsdf'
actions = []
for button in Buttons:
    action = {
        "name": button.get('title'),
        "integration": { "url": "", "context": {"action": button.get('payload')}}
    }
    actions.append(action)

attachments = []
attachment = {}
attachment['text']="This is text"
attachment['actions'] = actions
attachments.append(attachment)
props = {}
props['attachments'] = attachments
payload['props']=props
print(json.dumps(payload))