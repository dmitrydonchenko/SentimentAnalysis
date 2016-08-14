import facebook
import facebook_lib
import networkx as nx
import facebookuser
import dateutil.parser as dateparser
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# https://www.facebook.com/bbcnews/posts/10153826631687217
# https://www.facebook.com/BBCTravel/posts/1080149335338199 page_id = 33536249999517
#post_id = '228735667216_10153826631687217'
#parent_id = '10153826631687217_10153826631687217'

# 10153824057298951 10153835396938951 https://www.facebook.com/natgeo/posts/10153835396938951
post_id = '23497828950_10153824057298951'
parent_id = '10153835396938951_10153835396938951'

# получаем все комментарии поста
comments = facebook_lib.get_comments(post_id)

comments_data = comments["data"]

# создаем граф пользователей
users_graph = nx.DiGraph()

edges = { }
edge_id = 0

# добавляем вершины и ребра в граф
for comment in comments_data:
    # получаем пользователя, написавшего комментарий
    user = facebookuser.FacebookUser(comment['from']['id'], comment['from']['name'])
    # добавляем его в граф, если он еще не был добавлен
    if user not in users_graph:
        users_graph.add_node(user)
    # получаем пользователей, поставивших "лайк" этому комментарию
    if 'likes' in comment:
        if 'data' in comment['likes']:
            likes = comment['likes']['data']
            for like in likes:
                like_user = facebookuser.FacebookUser(like['id'], like['name'])
                # добавляем пользователя, поставившего лайк, в граф
                if like_user not in users_graph:
                    users_graph.add_node(like_user)
                # добавляем в граф ребро от пользователя, написавшего комментарий, к пользователю, который поставил лайк
                edge_direction = (user, like_user)
                if edge_direction not in edges:
                    edges[edge_direction] = facebookuser.Edge(edge_id, user, like_user, user.name + " - " + like_user.name, 1)
                    edge_id += 1
                else:
                    edges[edge_direction].weight += 1
                users_graph.add_edge(user, like_user, weight=0)
                if 'weight' in users_graph[user][like_user]:
                    users_graph[user][like_user]['weight'] = 1
                else:
                    users_graph[user][like_user]['weight'] += 1
    # если комментарий - ответ на другой комментарий, создаем ребро в графе
    # ребро - от пользователя, написавшего комментарий, к пользователю, который на него ответил
    if 'parent' in comment:
        # получаем пользователя, на комментарий которого ответили
        parent = comment['parent']['from']
        parent_user = facebookuser.FacebookUser(parent['id'], parent['name'])
        # добавляем его в граф
        if parent_user not in users_graph:
            users_graph.add_node(parent_user)
        # добавляем в граф ребро
        edge_direction = (parent_user, user)
        if edge_direction not in edges:
            edges[edge_direction] = facebookuser.Edge(edge_id, parent_user, user, parent_user.name + " - " + user.name, 5)
            edge_id += 1
        else:
            edges[edge_direction].weight += 5
        users_graph.add_edge(parent_user, user, weight=0)
        if 'weight' in users_graph[parent_user][user]:
            users_graph[parent_user][user]['weight'] += 5
        else:
            users_graph[parent_user][user]['weight'] = 5


# экспорт графа в csv-файл
nodes_file = open('nodes.csv', 'w+')
edges_file = open('edges.csv', 'w+')

nodes_file.write("Id,Label\r\n")
edges_file.write("Source,Target,Type,Id,Label,Weight\r\n")

nodes = users_graph.nodes()

for node in nodes:
    nodes_file.write(node.id + ',' + node.name + '\r\n')

for key, value in edges.items():
    edges_file.write(value.source.id + ',' + value.target.id + ',Directed,' + str(value.id) + ',' + value.name + ',' + str(value.weight) + '\r\n')

# анализ тональности комментариев

post_object = facebook_lib.get_object_by_id(post_id)
created_time_post = dateparser.parse(post_object['created_time'])
sentences_comments, time_comments = facebook_lib.get_comments_format(post_id)
timeX = facebook_lib.time_to_x(time_comments, created_time_post)
posY, negY, allY = facebook_lib.sentiment_analysis(sentences_comments)

# fi = plt.figure()
# # fig1 = plt.plot(timeX, posY, color = 'g')
# # fig2 = plt.plot(timeX, negY, color = 'r')
# ax1 = fi.add_subplot(111)
# ax2 = fi.add_subplot(111)
# ax1.plot(timeX, posY, color = 'g')
# ax2.plot(timeX, negY, color = 'r')
#
# # Draw annotate of graph
# posYannotate = 20 if posY[0] < 0.5 else -20
# negYannotate = 20 if negY[0] < 0.5 else -20
# index = len(timeX)- 1
# plt.annotate('Positive', xy=(timeX[index], posY[index]), xytext=(40,posYannotate),
#                 textcoords='offset points', ha='center', va='bottom',
#                 bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
#                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',
#                                 color='blue'))
# plt.annotate('Negative', xy=(timeX[index], negY[index]), xytext=(40,negYannotate),
#                 textcoords='offset points', ha='center', va='bottom',
#                 bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
#                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',
#                                 color='blue'))
#
# plt.xlabel('Time(s)')
# plt.ylabel('Sentiment analysis')
# fi.suptitle(post_object['message'])
# # Show graph
# plt.show()

fi = plt.figure()
# fig1 = plt.plot(timeX, posY, color = 'g')
# fig2 = plt.plot(timeX, negY, color = 'r')
#ax1 = fi.add_subplot(111)
#ax1.plot(timeX, allY, color = 'g', marker='o')
plt.scatter(timeX, allY)

# Draw annotate of graph
#allYannotate = 20 if allY[0] < 0.5 else -20
#index = len(timeX)- 1
# plt.annotate('Compound', xy=(timeX[index], allY[index]), xytext=(40,allYannotate),
#                 textcoords='offset points', ha='center', va='bottom',
#                 bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
#                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',
#                                 color='blue'))

plt.xlabel('Time(s)')
plt.ylabel('Sentiment analysis')
fi.suptitle(post_object['message'])
# Show graph
plt.show()






