import json
import difflib

# Data provided kindly by https://foodb.ca/
FOOD_DIR = "foodb_2020_04_07_json/Food.json"

# Housekeeping to prevent charmap errors (replace '\xa0' to ' ') and change to json list

f = open(FOOD_DIR,mode='r',encoding='utf8')
g = f.read().split('\n')[:-1]
g[0] = '[' + g[0] + ','
g[0] = g[0].replace(u'\xa0',u' ')
for i in range(1,len(g)-1):
    g[i] += ','
    g[i] = g[i].replace(u'\xa0',u' ')
g[-1] += ']'
g[-1] = g[-1].replace(u'\xa0',u' ')
jstring = '\n'.join(g)
data = json.loads(jstring)

food_groups = []

for i in data:
    if i["food_group"] not in food_groups:
        food_groups.append(i['food_group'])

COLD = ['Beverages', 'Aquatic foods', 'Animal foods', 'Milk and milk products', 'Eggs', 'Soy', 'Dishes']
FRESH = ['Vegetables', 'Fruits', 'Gourds']
DRY = ['Herbs and Spices', 'Herbs and spices', 'Nuts', 'Cereals and cereal products', 'Pulses', 'Teas', 'Coffee and coffee products', 'Cocoa and cocoa products', 'Confectioneries', 'Baking goods', 'Snack foods', 'Fats and oils']
OTHER = ['Baby foods', 'Unclassified', None]


def search(food):
    names = []
    for i in data:
        if food.upper() == i['name'].upper():
            return [i['name'].upper()]
        if food.upper() in i['name'].upper() or i['name'].upper() in food.upper():
            names.append(i['name'].upper())
    return names

# Returns a tuple of (type, foodname)
def item(food):
    x = search(food)
    elem = dict()
    for i in data:
        if i['name'].upper() == x[0]:
            elem = i
    return elem

def pretty_item(food):
    return json.dumps(item(food),indent=2)

# Grocery store order :: (DRY, FRESH, COLD, OTHER)
def order_dicts_by_food_group(foods):
    dry = []
    fresh = []
    cold = []
    other = []
    for i in foods:
        if i["food_group"] in COLD:
            cold.append(i["name"])
        elif i["food_group"] in FRESH:
            fresh.append(i["name"])
        elif i["food_group"] in DRY:
            dry.append(i["name"])
        else:
            other.append(i["name"])
    return dry, fresh, cold, other

print(search('milk (cow)'))
print(search('eggs'))
print(search('other candy'))
print(search('hamburger'))
print(search('water'))
print(search('common thyme'))
print(search('japanese pumpkin'))

df,ff,cf,of = order_dicts_by_food_group([item('milk (cow)'),item('eggs'),item('other candy'),item('hamburger'),item('water'),item('common thyme'),item('japanese pumpkin')])

print("*****DRY FOODS*****")
print('\n'.join(df))
print("****FRESH FOODS****")
print('\n'.join(ff))
print("****COLD FOODS*****")
print('\n'.join(cf))
print("*******OTHER*******")
print('\n'.join(of))










