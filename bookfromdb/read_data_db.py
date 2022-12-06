from sqlalchemy import create_engine, text


def read_next_id(id):
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost/celery_data"
    )

    with engine.connect() as con:
        rs = con.execute(
            text(
                f"""SELECT id, task_id, status, result \
                    FROM celery_taskmeta \
                    WHERE date_done > '2022.12.04 00:11:45' \
                    AND ID > {id}
                    ORDER BY ID
                    LIMIT 1
                """
            )
        )
        data = rs.fetchone()
    return data


if __name__ == "__main__":
    print(read_next_id(1658))
