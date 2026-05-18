import aiomysql
from config import Config


async def get_connection():
    return await aiomysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        autocommit=True
    )


async def get_new_orders(last_id: int) -> list[dict]:
    conn = await get_connection()

    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                SELECT id, bouquet, name, number, created_at
                FROM client
                WHERE id > %s
                ORDER BY id ASC
            """

            await cursor.execute(query, (last_id,))
            rows = await cursor.fetchall()

            result = []

            for row in rows:
                result.append({
                    "id": row["id"],
                    "bouquet_name": row["bouquet"],
                    "lead_name": row["name"],
                    "lead_phone": row["number"],
                    "created_at": str(row["created_at"])
                })

            return result

    finally:
        conn.close()