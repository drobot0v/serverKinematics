import requests as rq

resp01 = rq.get(url='http://127.0.0.1:5000/robot/m2RR')
print(resp01.text)

resp02 = rq.put(url='http://127.0.0.1:5000/robot/m2RR', 
                json= { 'num_of_joints': 3, 
                       'links' : { 0: { 'name': 'link01' } } })
print(resp02.text)

resp03 = rq.get(url='http://127.0.0.1:5000/robot/m2RR')
print(resp03.text)