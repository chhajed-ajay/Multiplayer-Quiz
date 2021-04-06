import socket
import select
from thread import *
import sys
import time
import random

# AF_NET is the address of the socket
# SOL_SOCKET means the type of the socket
#SOCK_STREAM means that the data or characters are read in a flow
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Setting up the server details and checks whether proper size of arguments are given

#These are the values that the client must be aware about
server.bind((socket.gethostname(), 1273))
server.listen(100)

list_of_clients=[]


Q = [" What is the Italian word for PIE? \n a.Mozarella b.Pasty c.Patty d.Pizza",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit b.Celsius c.Rankine d.Kelvin",
     " Which sea creature has three hearts? \n a.Dolphin b.Octopus c.Walrus d.Seal",
     " Who was the character famous in our childhood rhymes associated with a lamb? \n a.Mary b.Jack c.Johnny d.Mukesh",
     " How many bones does an adult human have? \n a.206 b.208 c.201 d.196",
     " How many wonders are there in the world? \n a.7 b.8 c.10 d.4",
     " What element does not exist? \n a.Xf b.Re c.Si d.Pa",
     " How many states are there in India? \n a.24 b.29 c.30 d.31",
     " Who invented the telephone? \n a.A.G Bell b.John Wick c.Thomas Edison d.G Marconi",
     " Who is Loki? \n a.God of Thunder b.God of Dwarves c.God of Mischief d.God of Gods",
     " Who was the first Indian female astronaut ? \n a.Sunita Williams b.Kalpana Chawla c.None of them d.Both of them ",
     " What is the smallest continent? \n a.Asia b.Antarctic c.Africa d.Australia",
     " The beaver is the national embelem of which country? \n a.Zimbabwe b.Iceland c.Argentina d.Canada",
     " How many players are on the field in baseball? \n a.6 b.7 c.9 d.8",
     " Hg stands for? \n a.Mercury b.Hulgerium c.Argenine d.Halfnium",
     " Who gifted the Statue of Libery to the US? \n a.Brazil b.France c.Wales d.Germany",
     " Which planet is closest to the sun? \n a.Mercury b.Pluto c.Earth d.Venus",
     " Who is the national animal of India? \n a.Tiger b.Peacock c.Lion d.Elephant",
     " What is the largest prime number less than 10? \n a.1 b.10 c.9 d.7",
     " Who is the prime minister of India? \n a.Arvind Kejriwal b.Narendra Singh Modi c.Rahul Gandhi d.Shahrukh Khan",
     " Which is the smallest country? \n a.China b.Pakistan c.Srilanka d.Wetican city",
     " Who is the vice captain of Indian team? \n a.Virat Kohli b.Umesh Yadav c.Ashish Nehra d.Rohit Sharma",
     " ACM competition in India is organised by? \n a.Codeforces b.Codechef c.Hackerrank d.Atcode",
     " Who discovered zero? \n a.Sri Dhranacharaya b.Aryabhatta c.Chetanaya d. Sri Dhronacharaya",
     " In which industry the oscard award is given? \n a.Tech. companies b.Business c.Cinema d.NGOs",
     " Average weight(in kg) for a normal man? \n a.50 b.60 c.70 d.65",
     " Who won the cricket world cup of 2019? \n a.Newzealand b.India c.Zimbabwe d.England",
     " Who is the president of America? \n a.Obama b.Trumph c.Cristano Ronaldo d.None of these",
     " When the first computer is invented? \n a.1983 b.1975 c.1980 d.1938",]

A = ['d', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'c', 'a', 'b', 'a', 'a', 'c', 'b', 'd', 'd', 'b', 'b', 'c', 'c', 'd', 'b', 'd']

Count=[]
client = ["address",-1]
bzr =[0, 0, 0] #Buzzer List

def clientthread(conn, addr):
    conn.send("Hello Genius!!!\n\nWelcome to this quiz! Answer any 5 questions correctly before your opponents do\nPress any key on the keyboard as a buzzer for the given question\n\n\n")
    #Intro MSG
    while True:
            message = conn.recv(2048)
            if message:
                if bzr[0]==0:
                    client[0] = conn # 'conn' is client socket here
                    bzr[0] = 1
                    i = 0
                    while i < len(list_of_clients):
                            if list_of_clients[i] == client[0]:
                                break
                            i +=1
                    client[1] = i

                elif bzr[0] ==1 and conn==client[0]:
                        bol = message[0] == A[bzr[2]][0]
                        print A[bzr[2]][0]
                        if bol:
                            Count[i] += 1
                            broadcast("Player" + str(client[1]+1) + " +1" + "\n\n\nPlayer 1 score is : " + str(Count[0]) + "\nPlayer 2 score is : " + str(Count[1]) + "\nPlayer 3 score is : " + str(Count[2])+"\n")
                            if Count[i]>=5:
                                broadcast("Player" + str(client[1]+1) + " WON" + "\n")
                                end_quiz()
                                sys.exit()

                        else:
                            Count[i] -= 0.5
                            broadcast("Player" + str(client[1]+1) + " -0.5" + "\n\n\nPlayer 1 score is : " + str(Count[0]) + "\nPlayer 2 score is : " + str(Count[1]) + "\nPlayer 3 score is : " + str(Count[2])+"\n")
                        bzr[0]=0
                        if len(Q) != 0:
                            Q.pop(bzr[2])
                            A.pop(bzr[2])
                        if len(Q)==0:
                            end_quiz()
                        quiz()

                else:
                        conn.send(" player " + str(client[1]+1) + " pressed buzzer first\n\n")
            else:
                    remove(conn)

def broadcast(message):
    for clients in list_of_clients:
        try:
            clients.send(message)
        except:
            clients.close()
            remove(clients)
def end_quiz():
        broadcast("Game Over\n")
        bzr[1]=1
        i = Count.index(max(Count))
        broadcast("player " + str(i+1)+ " wins!! by scoring "+str(Count[i])+" points.\n")
        for x in range(len(list_of_clients)):
            if(Count[x]>=5):
                list_of_clients[x].send("Well played player " + str(x+1) + ".You scored " + str(Count[x]) + " points.\n You have won the game.")    
            else:
                list_of_clients[x].send("You scored " + str(Count[x]) + " points.")
            
        server.close()


def quiz():
    bzr[2] = random.randint(0,10000)%len(Q) # bzer[2] is stroing a random integer, an index from which we are sending the questions
    if len(Q) != 0: # len Q finally will come to zero or one of the participants reach the score of 5 
        for connection in list_of_clients:
            connection.send(Q[bzr[2]])
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept() # server accept gives client socket and address
    list_of_clients.append(conn) # making list of all the clients
    Count.append(0) # making their starting count as 0 zero.
    print addr[0] + " connected" 
    start_new_thread(clientthread,(conn,addr))
    if(len(list_of_clients)==3): # if there are three participants then start the quiz
        k = 5
        broadcast("\nQuiz will start in 5 seconds.\nGet ready to fight......  ")
        while(k!=0):
            broadcast(str(k)+ " "),
            time.sleep(1)
            k-=1
        quiz() 
conn.close() 
server.close()
