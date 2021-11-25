from utils.ine_etl import extract_dict_ccaa, extract_dict_provinces, extract_dict_municipalities, extract_dict_metadata
from db_mongo.mongodb_management import conn_mongodb, create_unique_compound_index, insert_data

# Connect to client and database
client, db = conn_mongodb()

# Create uniques indexes for collections
idx_ine_dict_ccaa = create_unique_compound_index(database=db,
                                                 collection_name='ine_dict_ccaa',
                                                 fields=['CODAUTO', 'NOMBRE'],
                                                 index_name='codauto_nombre_idx')

idx_ine_dict_provinces = create_unique_compound_index(database=db,
                                                      collection_name='ine_dict_provinces',
                                                      fields=['CPRO', 'NOMBRE'],
                                                      index_name='cpro_nombre_idx')

idx_ine_dict_municipalities = create_unique_compound_index(database=db,
                                                           collection_name='ine_dict_municipalities',
                                                           fields=['CPRO', 'CMUN', 'NOMBRE'],
                                                           index_name='cpro_cmun_nombre_idx')

idx_ine_metadata = create_unique_compound_index(database=db,
                                                collection_name='ine_metadata',
                                                fields=['title', 'collections'],
                                                index_name='title_collections_idx')

# Create payload of data to insert
dict_ccaa = extract_dict_ccaa()
dict_provinces = extract_dict_provinces()
dict_municipalities = extract_dict_municipalities()
metadata = extract_dict_metadata()

# Insert data
insert_data(dict_ccaa, 'ine_dict_ccaa', db)
insert_data(dict_provinces, 'ine_dict_provinces', db)
insert_data(dict_municipalities, 'ine_dict_municipalities', db)
insert_data(metadata, 'ine_metadata', db)
