import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        # Variabili per ottenere l'oggetto selezionato dal dropdown
        self._store = None
        self._node = None



    def handleCreaGrafo(self, e):
        if self._store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona uno store dal dropdown", color = "red")
            )
            self._view.update_page()
            return

        k = self._view._txtIntK.value

        if k=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore nel campo k", color = "red")
            )
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore numerico nel campo k", color="red")
            )
            self._view.update_page()
            return

        if kInt<=0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore positivo di k", color = "red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(self._store, kInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )

        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        self.fillDdNodes()


        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi")
        )
        self._view.update_page()

        archiConPesoMaggiore = self._model.getArchiConPesoMaggiore()
        self._view.txt_result.controls.append(
            ft.Text("5 Archi di peso maggiore:")
        )
        for a in archiConPesoMaggiore:
            self._view.txt_result.controls.append(
                ft.Text(f"Arco: {a[0]} -> {a[1]} - Peso: {a[2]['weight']}")
            )
        self._view.update_page()




    def handleCerca(self, e):

        if self._node is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona uno nodo", color = "red")
            )
            self._view.update_page()
            return

        path = self._model.cercaPercorsoPiuLungo(self._node)
        self._view.txt_result.controls.append(
            ft.Text(f"Nodo di partenza: {self._node}")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.update_page()

    def handleRicorsione(self, e):
        if self._node is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona uno nodo", color = "red")
            )
            self._view.update_page()
            return

        self._model.getRicorsione(self._node)
        percorso = self._model._solBest
        self._view.txt_result.controls.append(
            ft.Text(f"Il peso maggiore è {self._model._costoBest}")
        )
        for p in percorso:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.update_page()



    def fillDdStores(self):
        stores = self._model.fillDdStores()
        for s in stores:
            self._view._ddStore.options.append(
                ft.dropdown.Option(
                    data = s,
                    key = s.store_id,
                    text = s.store_name,
                    on_click=self._choiceStore
                )
            )
        self._view.update_page()

    def _choiceStore(self, e):
        self._store = e.control.data


    def fillDdNodes(self):
        nodes = self._model.getNodes()
        nodes.sort(key = lambda x: x.order_id)
        for n in nodes:
            self._view._ddNode.options.append(
                ft.dropdown.Option(
                    data = n,
                    key = n.order_id,
                    text = n.order_id,
                    on_click = self._choiceNode
                )
            )
        self._view.update_page()

    def _choiceNode(self, e):
        self._node = e.control.data