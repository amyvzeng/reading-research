#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import natjoin


# In[2]:


aka_name = ["id", "person_id", "name", 
            "imdb_index", "name_pcode_cf", "name_pcode_nf", 
            "surname_code", "md5sum"]
aka_title = ["id", "movie_id", "title", 
             "imdb_index", "kind_id", "production_year", 
             "phonetic_code", "episode_of", "season_nr", 
             "episode_nr", "note", "md5sum"]
cast_info = ["id", "person_id", "movie_id",
            "person_role_id", "note", "nr_order",
            "role_id"]
char_name = ["id", "name", "imdb_index",
            "imdb_id", "name_pcode_nf", "surname_pcode",
            "md5sum"]
comp_cast_type = ["id", "kind"]
company_name = ["id", "name", "country_code",
               "imdb_id", "name_pcode_nf", "name_pcode_sf",
               "md5sum"]
company_type = ["id", "kind"]
complete_cast = ["id", "movie_id", "subject_id",
                "status_id"]
info_type = ["id", "info"]
keyword = ["id", "keyword", "phonetic_code"]
kind_type = ["id", "kind"]
link_type = ["id", "link"]
movie_companies = ["id", "movie_id", "company_id",
                  "company_type_id", "note"]
movie_info_idx = ["id", "movie_id", "info_type_id",
                 "info", "note"]
movie_keyword = ["id", "movie_id", "keyword_id"]
movie_link = ["id", "movie_id", "linked_movie_id",
             "link_type_id"]
name = ["id", "name", "imdb_index",
       "imdb_id", "gender", "name_pcode_cf",
       "name_pcode_nf", "surname_pcode", "md5sum"]
role_type = ["id", "role"]
title = ["id", "title", "imdb_index",
        "kind_id", "production_year", "imdb_id",
        "phonetic_code", "episode_of_id", "season_nr",
        "series_years", "md5sum"]
movie_info = ["id", "movie_id", "info_type_id",
             "info", "note"]
# person_info = ["id", "person_id", "info_type_id",
#               "info", "note"]


# In[3]:


csv_names = {"aka_name": aka_name, "aka_title": aka_title, "cast_info": cast_info, "char_name": char_name,
            "comp_cast_type": comp_cast_type, "company_name": company_name, "company_type": company_type, 
             "complete_cast": complete_cast, "info_type": info_type, "keyword": keyword, 
             "kind_type": kind_type, "link_type": link_type, "movie_companies": movie_companies, 
             "movie_info": movie_info, "movie_info_idx": movie_info_idx, "movie_keyword": movie_keyword, "movie_link": movie_link,
            "name": name, "role_type": role_type, "title": title, "movie_info": movie_info}


# In[4]:


csv_tables = {}

for csv_title in csv_names.keys():
    with open('./imdb/' + csv_title + '.csv', newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        table = []
        headers = csv_names[csv_title]
        counter = 0
        for row in spamreader:
            if counter >= 1000:
                break
            else:
                counter += 1
                table.append({headers[i]: row[i] for i in range(1, len(headers))})
    csv_tables[csv_title] = table


# In[5]:


sqlqueries = []
with open('sqlqueries.txt', 'r') as f:
    content = f.readlines()
    
for line in content:
    if line != "\n":
        sqlqueries.append(line.split("\n")[0])
        
queries = {}
for query in sqlqueries:
    select = query.split("SELECT ")[1].split(" FROM ")[0]
    from_tables = query.split(" FROM ")[1].split(" WHERE ")[0]
    attrs = query.split(" FROM ")[1].split(" WHERE ")[1]
#     print(select)
#     print(from_tables)
#     print(attrs)
#     print("\n")


# In[6]:


ct = csv_tables["company_type"].copy()
it = csv_tables["info_type"].copy()
mc = csv_tables["movie_companies"].copy()
mi_idx = csv_tables["movie_info_idx"].copy()
t = csv_tables["title"].copy()
cn = csv_tables["company_name"].copy()
mk = csv_tables["movie_keyword"].copy()
mi = csv_tables["movie_info"].copy()
k = csv_tables["keyword"].copy()


# In[7]:


def find_min(table, key):
    min_val = table[0][key]
    for entry in table:
        if entry[key] < min_val and entry[key] != '':
            min_val = entry[key]
    return min_val


# In[8]:


def replace_key(table, original_key, new_key):
    for entry in table:
        entry[new_key] = entry[original_key]
        #print(entry[original_key])
        #del entry[original_key]
    return table


# In[9]:


def insert_key(table, new_key):
    counter = 1
    for entry in table:
        entry[new_key] = counter
        counter+=1
    return table


# In[10]:


mc = replace_key(mc, "company_type_id", "id")
t3 = natjoin.natural_join([mc, ct])


# In[11]:


t1 = natjoin.natural_join([csv_tables["movie_companies"], csv_tables["movie_info_idx"]])


# In[ ]:


cn = insert_key(cn, "company_id")
t2 = natjoin.natural_join([cn, csv_tables["movie_companies"]])


# In[ ]:


mk = replace_key(mk, "movie_id", "id")
t4 = natjoin.natural_join([mk, t])


# In[ ]:


# mk = csv_tables["movie_keyword"].copy()
# t5 = natjoin.natural_join([mk, mi_idx])


# # In[ ]:


# mk = replace_key(mk, "keyword_id", "id")
# t6 = natjoin.natural_join([mk, k])
# print(t6)


# # In[ ]:


# mc = replace_key(csv_tables["movie_companies"], "movie_id", "id")
# t7 = natjoin.natural_join([t, mc])
# print(t7)


# # In[ ]:


# t8 = natjoin.natural_join([csv_tables["company_info"], csv_tables["movie_keyword"]])


# # In[ ]:


# ci = csv_tables["company_info"]
# replace_key(ci, "person_id", "id")
# t9 = natjoin.natural_join([ci, csv_tables["name"]])


# In[ ]:


# print(t6)


# In[ ]:




