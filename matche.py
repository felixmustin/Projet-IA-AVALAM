import cherrypy
import sys
import copy
import json
import socket

inf = float("inf")

#Liste content toutes les combinaisons possibles de tuples de type ((x, y),(x,y))
toutcoups=[] 
for x in range(0, 9):
    r1 = x
    for y in range(0, 9):
        c1 = y
        for o in range(0, 9):
            r2 = o
            for b in range(0, 9):
                c2 = b
                previous = (r1, c1)
                nextt = (r2, c2)
                toutcoups.append((previous, nextt))


class Game():
    #Renvoie False si le coup est sur une case voisine, True si le coup est valide
    def play(self, coups):
        prev = coups[0]
        nex = coups[1]
        if nex[0] == prev[0]:
            if nex[1] == int(prev[1]+1):
                return True
            elif nex[1] == int(prev[1]-1):
                return True
            else:
                return False

        elif nex[0] == int(prev[0] -1):
            if nex[1] == prev[1]:
                return True
            elif nex[1] == int(prev[1] +1):
                return True
            elif nex[1] == int(prev[1]-1):
                return True
            else:
                return False

        elif nex[0] == int(prev[0] +1):
            if nex[1] == prev[1]:
                return True
            elif nex[1] == int(prev[1] +1):
                return True
            elif nex[1] == int(prev[1]-1):
                return True
            else:
                return False
        else:
            return False

    #Renvoie False si la pile de pions ne dépasse pas 5 ou si la case n'est pas vide, True si le coup est valide
    def case(self, state, coups):
        prev = coups[0]
        nex = coups[1]
        nbr_prev = len(state[0][prev[0]][prev[1]])
        nbr_nex = len(state[0][nex[0]][nex[1]])
        if prev == nex:
            return False
        elif nbr_prev == 0:
            return False
        elif nbr_nex == 0:
            return False
        elif nbr_prev + nbr_nex > 5:
            return False
        else:
            return True

    #Calcule le score pour un état donné 'state'
    def utility(self, state, x, y):
        score = 0
        for elem in state:
            for elem2 in elem:
                for elem3 in elem2:
                    i = len(elem3)
                    if i != 0:
                        if elem3[-1] == x:
                            score += 1
                        elif elem3[-1] == y:
                            score -= 1
                    if i == 5:
                        if elem3[-1] == x:
                            score += 2
                        elif elem3[-1] == y:
                            score -= 2
        return score

    #Renvoie True 'play' et 'case' renvoient True pour un coup et son état de jeu
    def available_move(self, state, coups):
        if self.play(coups):
            if self.case(state, coups):
                return True
            else:
                return False
        else:
            return False

    #Renvoie tout les coups possibles pour un état donné
    def get_available_moves(self, state):
        return ([a for a in toutcoups if self.available_move(state, a)==True])

    #Renvoie l'état modifié après avoir joué un coup donné 'move'
    def next_state(self, state, coup):
        nextstate = copy.deepcopy(state)
        nextstate[0][coup[1][0]][coup[1][1]] = nextstate[0][coup[1][0]][coup[1][1]] + copy.deepcopy(nextstate[0][coup[0][0]][coup[0][1]])
        del nextstate[0][coup[0][0]][coup[0][1]]
        nextstate[0][coup[0][0]].insert(coup[0][1], [])
        return nextstate

    # Renvoie True si plus aucun coup n'est possible sur l'état 'state'      
    def is_finished(self, state):
        if len(self.get_available_moves(state))==0:
            return True
        else:
            return False
    
    #Algorithme MinMax
    def search(self, state, x, y, prune=True):
        def max_value(self, state, alpha, beta, depth):
            if self.is_finished(state) or depth == 2:
                return self.utility(state, x, y), None
            val = -inf
            action = None
            for moves in self.get_available_moves(state):
                clone = self.next_state(state, moves)
                v, _= min_value(self, clone, alpha, beta, depth+1)
                if v > val:
                    val = v
                    action = moves
                    if prune:
                        if v >= beta:
                            return v, moves
                        alpha = max(alpha, v)
            return val, action

        def min_value(self, state, alpha, beta, depth):
            if self.is_finished(state) or depth == 2:
                return self.utility(state, x, y), None
            val = inf
            action = None
            for moves in self.get_available_moves(state):
                clone = self.next_state(state, moves)
                v, _ = max_value(self, clone, alpha, beta, depth+1)
                if v < val:
                    val = v
                    action = moves
                    if prune:
                        if v <= alpha:
                            return v, moves
                        beta = min(beta, v)
            return val, action

        _, action = max_value(self,state, -inf, inf, 0)
        return action


class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
    
        body = cherrypy.request.json
        game = body["game"]
        l=[]
        l.append(game)

        #Changer le x et y pour inverser le score dans la fonction utility
        if body["players"][0] == body["you"]:
            x = 0
            y = 1
        elif body["players"][1] == body["you"]:
            x = 1
            y = 0
        
        G = Game()
        coup = G.search(l, x, y)
        preced = coup[0]
        proch = coup[1]
        response = {"move": {"from": [preced[0], preced[1]], "to": [proch[0], proch[1]]}, "message": "Coup effectué"}
        return response

    @cherrypy.expose
    def ping(self):
        return "pong"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': port})
    cherrypy.quickstart(Server())
