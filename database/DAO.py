from database.DB_connect import DBConnect
from model.edge import Edge
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                    from orders o, stores s
                    where s.store_id = o.store_id and s.store_id = %s"""

        cursor.execute(query, (store.store_id, ))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(store, k, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        # RICORDA !! Per il join devi fare join tabella_su_cui_vuoi_joinare on condizione_join

        # In questo caso fai from (query annidata che restituisce per gli ordini di un dato store: id, data e
        # quantita (relazione uno a molti tra orders e orders_item) e la chiami o1, e poi fai il join su una
        # tabella uguale che chiami o2 con condizione o1.order_date<o2.order_date perchè l'arco va sempre
        # dall'ordine effettutao in data precedente o1 a quello in data successiva o2 (ed essendo id la chiave
        # primaria dell'ordine, se la data è diversa, anche gli ordini sono diversi).
        # Infine metti nel where la condizione èper la differenza tra la date
        query = """SELECT o1.order_id AS order_id1, o2.order_id AS order_id2, 
                   ((SUM(oi.quantity) + SUM(oi2.quantity)) / DATEDIFF(o2.order_date, o1.order_date)) AS peso
                    FROM 
                        orders o1, orders o2, order_items oi, order_items oi2
                    WHERE 
                        o1.store_id = %s
                        AND o1.store_id = o2.store_id
                        AND oi.order_id = o1.order_id
                        AND oi2.order_id = o2.order_id
                        AND o1.order_date < o2.order_date
                        AND DATEDIFF(o2.order_date, o1.order_date) <= %s
                    GROUP BY 
                        o1.order_id, o2.order_id"""

        cursor.execute(query, (store.store_id, k))

        for row in cursor:
            results.append(Edge(
                idMap[row["order_id1"]],
                idMap[row["order_id2"]],
                row["peso"]
            ))

        cursor.close()
        conn.close()
        return results
