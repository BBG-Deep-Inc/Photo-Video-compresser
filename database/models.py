from sqlalchemy import Table,Column,MetaData,Boolean,String


metadata_obj = MetaData()

main_table = Table(
    "main_table",
    metadata_obj,
    Column("username",String,primary_key=True),
    Column("sub",Boolean)
)