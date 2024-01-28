from django.db import connection
from django.http import JsonResponse

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