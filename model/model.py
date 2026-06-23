import copy

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._solBest = []
        self._costoBest = 0



    def fillDdStores(self):
        stores = DAO.getAllStores()
        return stores

    def buildGraph(self, store, k):
        self.addNodes(store)
        self.addEdges(k, store)


    def addNodes(self, store):
        nodes = DAO.getAllNodes(store)
        for node in nodes:
            self._idMap[node.order_id] = node
        self._graph.add_nodes_from(nodes)

    def addEdges(self, k, store):
        edges = DAO.getAllEdges(store, k, self._idMap)
        for edge in edges:
            self._graph.add_edge(edge.order1, edge.order2, weight=edge.peso)

    def getArchiConPesoMaggiore(self):
        if (len(self._graph.edges))<5:
            return self._graph.edges
        # RICORDA!!!! data=True altrimenti non puoi considerare il peso
        topArchi = sorted(self._graph.edges(data=True), key=lambda edge: edge[2]["weight"], reverse=True)
        return topArchi[0:5]


    # Cerca il percorso più lungo (peso maggiore), partendo da un dato nodo
    def cercaPercorsoPiuLungo(self, nodeSource):
        # METODO PIU CORTO
        #tree = nx.dfs_tree(self._graph, nodeSource)
        #lp = nx.dag_longest_path(tree)
        #return lp


        #for source in self._graph.nodes:
        tree = nx.dfs_tree(self._graph, nodeSource)
        nodi = list(tree.nodes())
        lp = []


        for node in nodi:
            tmp = [node]
            # Per ogni nodo risale l'albero verso la sorgente
            # Parte dal nodo corrente [node]
            # Ad ogni iterazione trova il predecessore e lo inserisce in testa
            # Si ferma quando arriva a nodeSource
            while tmp[0] != nodeSource:
                pred = nx.predecessor(tree, nodeSource, tmp[0])
                tmp.insert(0, pred[0])

            # Alla fine tmp contiene il cammino completo [nodeSource, ..., node].
            # Se il cammino trovato è più lungo del migliore attuale,
            # lo salva con deepcopy per evitare che modifiche future a tmp alterino lp.

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp

    def getRicorsione(self, nodeSource):
        self._solBest = []
        self._costoBest = 0
        parziale=[]
        parziale.append(nodeSource)
        # Inizializzo a infinito il peso precdente, cosi sicuramente sara minore il peso dell'arco corrente
        # alla prima iterazione
        self._ricorsione(parziale, float('inf'))


    def _ricorsione(self, parziale, peso_precedente):

        if self._calcolaCosto(parziale) >= self._costoBest:
            self._solBest = copy.deepcopy(parziale)
            self._costoBest = self._calcolaCosto(parziale)


        # Consideri i successori del nodo corrente (nodes) e itero sui vicini
        for vicino in self._graph.successors(parziale[-1]):

            # Visto che vicino è un vicino di node, sono sicuramente collegati da un arco, a cui accedo così:
            peso_arco = self._graph[parziale[-1]][vicino]['weight']

            # Verifico che il peso corrente dell'arco sia minore del peso dell'arco precedente

            if peso_arco < peso_precedente and vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione(parziale, peso_arco)
                parziale.pop()




    def _calcolaCosto(self, parziale):

        somma = 0

        # In parziale ho nodi che sono sempre collegati da archi quindi iterando in parziale
        # posso accedere come segue all'arco (e al suo peso)
        # RICORDA!! se avessi nodi sparsi e non so se sono collegati da archi non posso accedervi come sotto
        for i in range(len(parziale)-1):
            somma = somma + self._graph[parziale[i]][parziale[i+1]]["weight"]
        return somma






    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getNodes(self):
        return list(self._graph.nodes)