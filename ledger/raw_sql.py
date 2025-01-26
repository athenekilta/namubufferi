from django.db import connection
from django.http import JsonResponse
from datetime import date

def get_product_data(start_date: date, end_date: date):
    query = """
    SELECT 
        lp.id AS product_id,
        lp.name AS product_name,
        lp.price AS product_price,
        SUM(CASE WHEN lt.quantity > 0 THEN lt.quantity ELSE 0 END) AS total_added_quantity,
        SUM(CASE WHEN lt.quantity < 0 THEN ABS(lt.quantity) ELSE 0 END) AS total_sold_quantity,
        SUM(lt.quantity) AS net_quantity_change
    FROM 
        ledger_product lp
    INNER JOIN 
        ledger_transaction lt ON lp.id = lt.product_id
    WHERE 
        lt.timestamp BETWEEN %s AND %s
    GROUP BY 
        lp.id, lp.name
    ORDER BY 
        product_name ASC
    LIMIT 500;
    """

    with connection.cursor() as cursor:
        # Execute query with start_date and end_date as parameters
        cursor.execute(query, [start_date, end_date])
        rows = cursor.fetchall()

    # Convert query result into a list of dictionaries
    results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    return JsonResponse(results, safe=False)
    
def get_debts():
    
    query = """
            SELECT 
                uu.id AS user_id,
                uu.username,
                uu.first_name,
                uu.last_name,
                SUM(lt.price * lt.quantity) AS total_paid
            FROM 
                users_user uu
            INNER JOIN 
                ledger_account la ON uu.id = la.user_id
            INNER JOIN 
                ledger_transaction lt ON la.id = lt.account_id
            GROUP BY 
                uu.id, uu.username, uu.first_name, uu.last_name
            HAVING 
                SUM(lt.price * lt.quantity) < 0
            ORDER BY 
                total_paid ASC
            LIMIT 5;
            """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Convert query results into dictionary
    results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    return JsonResponse(results, safe=False)