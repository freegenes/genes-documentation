from utils import *
import time
orders = getAllShopifyOrders(fulfillment_status="fulfilled")

yesPar = {'name': 'Participate in Bionet', 'value': 'Yes'}
noPar = {'name': 'Participate in Bionet', 'value': 'No'}
blankContact = {'name': 'Bionet Contact', 'value': 'NA'}

for o in orders:
    c=False
    fields = [a.to_dict()["name"] for a in o.note_attributes]
    if not noPar["name"] in fields:
        o.note_attributes.append(shopify.NoteAttribute(noPar))
        c = True
    if not blankContact["name"] in fields:
        c = True
        o.note_attributes.append(shopify.NoteAttribute(blankContact))
    if c:
        o.save()
        time.sleep(1)
bionet = {}
for o in orders:
    fields = {a.to_dict()["name"]: a.to_dict()["value"] for a in o.note_attributes}
    if fields[noPar["name"]]=="Yes" and o.attributes["fulfillment_status"]=="fulfilled":
        print(fields)
        info = (o.attributes["customer"].attributes["first_name"], o.attributes["customer"].attributes["last_name"], fields["Bionet Contact"])
        for l in o.line_items:
            if not l.attributes["product_id"] in bionet.keys():
                bionet[l.attributes["product_id"]] = []
            bionet[l.attributes["product_id"]] = list(set(bionet[l.attributes["product_id"]] + [info]))
print(bionet)
